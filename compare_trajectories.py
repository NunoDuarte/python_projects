"""
compare_trajectories.py
=======================
Runs the Khatib-APF trajectory optimizer 3 times, each with different
obstacle parameters, and shows all 3 resulting trajectories on the same
animated plot.

Trajectory colour convention
  RED    – Scenario 1 (strong obstacle)
  YELLOW – Scenario 2 (medium obstacle)
  GREEN  – Scenario 3 (weak obstacle)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
from scipy.optimize import minimize

# --------------------------------------------------------------------------- #
#  Arm Physical Parameters                                                      #
# --------------------------------------------------------------------------- #
l1, l2 = 1.0, 1.0      # Link lengths (m)
m1, m2 = 1.0, 1.0      # Link masses  (kg)
tau_max = 20.0          # Hard joint-torque limit (N.m)

# --------------------------------------------------------------------------- #
#  Three Obstacle Scenarios                                                     #
#  (label, r_obs, rho_0, eta_rep, w_vel_pot, traj_color, patch_alpha)          #
# --------------------------------------------------------------------------- #
p_obs = np.array([0.8, 1.0])   # Fixed obstacle centre for all scenarios

SCENARIOS = [
    ("Strong",  0.20, 0.60, 100.0,  1000,  "red",       0.40),
    ("Normal",  0.20, 0.40, 10.0,  500,  "yellow",    0.30),
    ("Weak",    0.20, 0.20, 1.0,  200,  "limegreen", 0.20),
]

# --------------------------------------------------------------------------- #
#  Kinematics & Dynamics                                                        #
# --------------------------------------------------------------------------- #

def forward_kinematics(q1, q2):
    x1, y1 = l1 * np.cos(q1), l1 * np.sin(q1)
    x2 = x1 + l2 * np.cos(q1 + q2)
    y2 = y1 + l2 * np.sin(q1 + q2)
    return np.array([0.0, 0.0]), np.array([x1, y1]), np.array([x2, y2])


def inverse_kinematics(x, y):
    r2 = x**2 + y**2
    cos_q2 = np.clip((r2 - l1**2 - l2**2) / (2 * l1 * l2), -0.999, 0.999)
    q2 = np.arccos(cos_q2)
    q1 = np.arctan2(y, x) - np.arctan2(l2 * np.sin(q2), l1 + l2 * np.cos(q2))
    return np.array([q1, q2])


def compute_dynamics(q, dq, d2q):
    q1, q2 = q[0], q[1]
    dq1, dq2 = dq[0], dq[1]
    d2q1, d2q2 = d2q[0], d2q[1]

    lc1, lc2 = l1 / 2.0, l2 / 2.0
    I1 = m1 * l1**2 / 12.0
    I2 = m2 * l2**2 / 12.0

    M11 = m1*lc1**2 + I1 + m2*(l1**2 + lc2**2 + 2*l1*lc2*np.cos(q2)) + I2
    M12 = m2*(lc2**2 + l1*lc2*np.cos(q2)) + I2
    M22 = m2*lc2**2 + I2

    h  = -m2 * l1 * lc2 * np.sin(q2)
    C1 = h * dq2 * dq1 + h * (dq1 + dq2) * dq2
    C2 = -h * dq1**2

    g1 = (m1*lc1 + m2*l1) * 9.81 * np.cos(q1) + m2*lc2 * 9.81 * np.cos(q1+q2)
    g2 = m2 * lc2 * 9.81 * np.cos(q1 + q2)

    return np.array([M11*d2q1 + M12*d2q2 + C1 + g1,
                     M12*d2q1 + M22*d2q2 + C2 + g2])

# --------------------------------------------------------------------------- #
#  Khatib (1986) Repulsive Potential – per-scenario parameters                 #
# --------------------------------------------------------------------------- #

def repulsive_potential(ee_pos, r_obs, rho_0, eta_rep):
    dist = np.linalg.norm(ee_pos - p_obs) - r_obs
    effective_dist = max(dist, 1e-4)
    if dist <= rho_0:
        u = 0.5 * eta_rep * ((1.0 / effective_dist) - (1.0 / rho_0))**2
        if dist < 1e-4:
            u += 1e5 * (1e-4 - dist)
        return u
    return 0.0


def ee_in_collision(ee_pos, r_obs):
    return np.linalg.norm(ee_pos - p_obs) <= r_obs

# --------------------------------------------------------------------------- #
#  Quintic-Basis Trajectory                                                     #
# --------------------------------------------------------------------------- #

def get_trajectory(params, qA, qB, N=100, K=4):
    T  = params[0]
    c1 = params[1: 1+K]
    c2 = params[1+K: 1+2*K]

    s = np.linspace(0, 1, N)
    s2, s3, s4, s5 = s**2, s**3, s**4, s**5

    q_base  = 10*s3 - 15*s4 + 6*s5
    dq_base = 30*s2 - 60*s3 + 30*s4

    q1  = qA[0] + (qB[0]-qA[0]) * q_base
    q2  = qA[1] + (qB[1]-qA[1]) * q_base
    dq1 = (qB[0]-qA[0]) * dq_base / T
    dq2 = (qB[1]-qA[1]) * dq_base / T

    for k in range(K):
        p_val = k + 3
        b  = s**p_val * (1-s)**3
        db = p_val * s**(p_val-1) * (1-s)**3 - 3 * s**p_val * (1-s)**2
        q1  += c1[k] * b;  q2  += c2[k] * b
        dq1 += c1[k] * db / T;  dq2 += c2[k] * db / T

    t_grid = s * T
    d2q1 = np.gradient(dq1, t_grid)
    d2q2 = np.gradient(dq2, t_grid)

    q   = np.vstack([q1, q2])
    dq  = np.vstack([dq1, dq2])
    d2q = np.vstack([d2q1, d2q2])

    tau = np.zeros_like(q)
    for i in range(N):
        tau[:, i] = compute_dynamics(q[:, i], dq[:, i], d2q[:, i])

    return T, t_grid, q, dq, tau

# --------------------------------------------------------------------------- #
#  Optimiser (per scenario)                                                    #
# --------------------------------------------------------------------------- #

def optimize_trajectory(pA, pB, r_obs, rho_0, eta_rep, w_vel_pot,
                         label="", K=4, max_retries=6):
    qA = inverse_kinematics(pA[0], pA[1])
    qB = inverse_kinematics(pB[0], pB[1])
    print(f"\n[{label}]  r_obs={r_obs}  rho_0={rho_0}  eta={eta_rep}  optimising...")

    def cost_func(x):
        T, t, q, dq, tau = get_trajectory(x, qA, qB, N=40, K=K)
        dt = T / 39.0
        effort = np.sum(tau**2) * dt

        u_rep = vel_pot = 0.0
        ee_list = [forward_kinematics(q[0,i], q[1,i])[2] for i in range(len(t))]
        for i in range(len(t)):
            u = repulsive_potential(ee_list[i], r_obs, rho_0, eta_rep)
            u_rep += u * dt
            if 0 < i < len(t)-1:
                v_ee = (ee_list[i+1] - ee_list[i-1]) / (2.0*dt)
                vel_pot += u * np.sum(v_ee**2) * dt
        return 1.5*T + 0.05*effort + u_rep + w_vel_pot*vel_pot

    def torque_constraint(x):
        T, t, q, dq, tau = get_trajectory(x, qA, qB, N=25, K=K)
        return np.hstack([tau_max - np.abs(tau[0]),
                          tau_max - np.abs(tau[1])])

    bounds      = [(0.2, 10.0)] + [(-15, 15)] * (2*K)
    constraints = [{'type': 'ineq', 'fun': torque_constraint}]

    # Deterministic starting points covering short, medium, and long durations
    initial_guesses = [
        [1.0] + [0.0]*(2*K),
        [1.5] + [0.0]*(2*K),
        [2.5] + [0.0]*(2*K),
        [3.5] + [0.0]*(2*K),
        [5.0] + [0.0]*(2*K),
        [7.0] + [0.0]*(2*K),
    ]
    # Fill remaining retries with diverse random guesses
    np.random.seed(42)
    for _ in range(max_retries - len(initial_guesses)):
        t_guess = np.random.uniform(1.0, 8.0)
        c_guess = list(np.random.uniform(-5.0, 5.0, 2*K))
        initial_guesses.append([t_guess] + c_guess)

    best_success = None   # best feasible (no collision, no torque violation)
    best_success_cost = float('inf')
    fallback_result = None  # best infeasible (used only if nothing feasible found)

    for attempt_idx, x0 in enumerate(initial_guesses):
        res = minimize(cost_func, x0, bounds=bounds,
                       constraints=constraints, method='SLSQP')
        T, t_grid, q, dq, tau = get_trajectory(res.x, qA, qB, N=100, K=K)

        has_collision = False
        fail_frame = len(t_grid) - 1
        for i in range(len(t_grid)):
            _, _, ee = forward_kinematics(q[0,i], q[1,i])
            if ee_in_collision(ee, r_obs):
                has_collision = True
                fail_frame    = i
                break

        torque_exceeded = np.max(np.abs(tau)) > (tau_max + 0.1)
        is_success = res.success and not has_collision and not torque_exceeded

        status_str = "OK" if is_success else ("COLLISION" if has_collision else ("TAU" if torque_exceeded else "SOLVER"))
        print(f"    attempt {attempt_idx+1:>2}/{len(initial_guesses)}  T={T:.2f}s  [{status_str}]")

        if is_success:
            cc = cost_func(res.x)
            if cc < best_success_cost:
                best_success_cost = cc
                best_success = (T, t_grid, q, dq, tau, True, fail_frame, attempt_idx+1)
            break  # first success is enough, stop trying
        else:
            # Keep as fallback only if better than current fallback
            if fallback_result is None:
                fallback_result = (T, t_grid, q, dq, tau, False, fail_frame, attempt_idx+1)

    best_result = best_success if best_success is not None else fallback_result

    T, t_grid, q, dq, tau, is_success, fail_frame, attempts = best_result
    if is_success:
        print(f"  SUCCESS (attempt #{attempts})  T={T:.2f}s")
    else:
        print(f"  FAILED after {attempts} attempts – violation at frame {fail_frame}")
    return T, t_grid, q, dq, tau, is_success, fail_frame

# --------------------------------------------------------------------------- #
#  Multi-Trajectory Visualisation                                               #
# --------------------------------------------------------------------------- #

def visualize_multi(pA, pB):
    # ---- run optimiser for each scenario ---------------------------------- #
    results = []
    for (label, r_obs, rho_0, eta_rep, w_vel_pot, color, alpha) in SCENARIOS:
        T, t_grid, q, dq, tau, is_success, fail_frame = \
            optimize_trajectory(pA, pB, r_obs, rho_0, eta_rep, w_vel_pot, label=label)

        N = len(t_grid)
        ee_x = np.zeros(N);  ee_y = np.zeros(N)
        for i in range(N):
            _, _, p2 = forward_kinematics(q[0,i], q[1,i])
            ee_x[i], ee_y[i] = p2

        vx   = np.gradient(ee_x, t_grid)
        vy   = np.gradient(ee_y, t_grid)
        v_ee = np.hypot(vx, vy)

        results.append(dict(
            label=label, color=color, alpha=alpha,
            r_obs=r_obs, rho_0=rho_0,
            T=T, t_grid=t_grid, q=q, dq=dq, tau=tau,
            ee_x=ee_x, ee_y=ee_y, v_ee=v_ee,
            is_success=is_success, fail_frame=fail_frame,
        ))

    # ---- figure layout ---------------------------------------------------- #
    fig = plt.figure(figsize=(16, 8))
    fig.patch.set_facecolor('#0d0d1f')

    ax_arm    = plt.subplot2grid((3, 3), (0, 0), rowspan=3)
    ax_ee_vel = plt.subplot2grid((3, 3), (0, 1), colspan=2)
    ax_vel    = plt.subplot2grid((3, 3), (1, 1), colspan=2)
    ax_trq    = plt.subplot2grid((3, 3), (2, 1), colspan=2)

    panel_bg = '#12122a'
    for ax in [ax_arm, ax_ee_vel, ax_vel, ax_trq]:
        ax.set_facecolor(panel_bg)
        ax.tick_params(colors='#aaaacc')
        for sp in ax.spines.values():
            sp.set_edgecolor('#333355')
        ax.xaxis.label.set_color('#aaaacc')
        ax.yaxis.label.set_color('#aaaacc')
        ax.title.set_color('#ddddff')

    # ---- arm workspace ---------------------------------------------------- #
    reach = l1 + l2 + 0.25
    ax_arm.set_xlim(-reach, reach)
    ax_arm.set_ylim(-reach, reach)
    ax_arm.set_aspect('equal')
    ax_arm.grid(True, linestyle='--', alpha=0.2, color='#555599')
    ax_arm.set_title("2-DOF Arm — 3 Obstacle Scenarios", fontweight='bold', fontsize=12)

    ax_arm.plot(pA[0], pA[1], 'o', color='white', ms=11,
                markeredgecolor='#00ffcc', markeredgewidth=2, zorder=8, label='Start A')
    ax_arm.plot(pB[0], pB[1], '*', color='white', ms=15,
                markeredgecolor='#ff88ff', markeredgewidth=2, zorder=8, label='Target B')

    # Draw legend with arrival times
    legend_patches = []
    for sc in results:
        c   = sc['color']
        r   = sc['r_obs']
        rho = sc['rho_0']
        obs_patch = plt.Circle(p_obs, r,       color=c, alpha=0.35, zorder=5)
        inf_patch = plt.Circle(p_obs, r + rho, color=c, alpha=0.20,
                               linestyle='--', fill=False, lw=1.8, zorder=5)
        ax_arm.add_patch(obs_patch)
        ax_arm.add_patch(inf_patch)
        legend_patches.append(
            mpatches.Patch(color=c, alpha=0.85,
                           label=f"{sc['label']}  T={sc['T']:.2f}s  (ρ₀={rho})"))

    # static EE ghost paths
    for sc in results:
        slc = slice(0, sc['fail_frame'] + 1)
        ax_arm.plot(sc['ee_x'][slc], sc['ee_y'][slc],
                    '--', color=sc['color'], alpha=0.35, lw=1.5)

    ax_arm.legend(handles=legend_patches, loc='lower left', fontsize=8,
                  facecolor='#1a1a30', edgecolor='#555588', labelcolor='white')

    # Timer display on workspace
    time_text = ax_arm.text(0.05, 0.95, "", transform=ax_arm.transAxes,
                            color='#ffffff', fontsize=12, fontweight='bold',
                            verticalalignment='top',
                            bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a30', edgecolor='#555588', alpha=0.85))

    # animated arm segments
    arm_lines  = []
    fail_marks = []
    for sc in results:
        ln, = ax_arm.plot([], [], 'o-', lw=4, ms=8, color=sc['color'],
                          alpha=0.90, zorder=7)
        mk, = ax_arm.plot([], [], 'X', ms=16, color=sc['color'],
                          markeredgecolor='white', markeredgewidth=2, zorder=9)
        arm_lines.append(ln)
        fail_marks.append(mk)

    # Global time limit across all 3 scenarios
    T_max = max(sc['T'] for sc in results)

    # ---- EE speed --------------------------------------------------------- #
    ax_ee_vel.set_title("End-Effector Speed  (reduced inside APF region)", fontsize=10)
    ax_ee_vel.set_ylabel("Speed (m/s)")
    ax_ee_vel.set_xlim(0, T_max * 1.05)
    ax_ee_vel.grid(True, linestyle='--', alpha=0.2, color='#555588')
    ee_dots = []
    for sc in results:
        slc = slice(0, sc['fail_frame'] + 1)
        ax_ee_vel.plot(sc['t_grid'][slc], sc['v_ee'][slc],
                       color=sc['color'], lw=1.8, alpha=0.9, label=f"{sc['label']} (T={sc['T']:.2f}s)")
        dot, = ax_ee_vel.plot([], [], 'o', color=sc['color'], ms=8)
        ee_dots.append(dot)
    ax_ee_vel.legend(fontsize=8, facecolor='#1a1a30',
                     edgecolor='#555588', labelcolor='white')

    # ---- joint velocities ------------------------------------------------- #
    ax_vel.set_title("Joint Velocities   solid=θ̇₁   dashed=θ̇₂", fontsize=10)
    ax_vel.set_ylabel("Velocity (rad/s)")
    ax_vel.set_xlim(0, T_max * 1.05)
    ax_vel.grid(True, linestyle='--', alpha=0.2, color='#555588')
    vel_dots = []
    for sc in results:
        slc = slice(0, sc['fail_frame'] + 1)
        ax_vel.plot(sc['t_grid'][slc], sc['dq'][0, slc],
                    '-',  color=sc['color'], lw=1.6, alpha=0.9)
        ax_vel.plot(sc['t_grid'][slc], sc['dq'][1, slc],
                    '--', color=sc['color'], lw=1.4, alpha=0.55)
        dot, = ax_vel.plot([], [], 'o', color=sc['color'], ms=8)
        vel_dots.append(dot)

    # ---- torques ---------------------------------------------------------- #
    ax_trq.set_title("Joint Torques   solid=τ₁   dashed=τ₂   (hard cap in crimson)", fontsize=10)
    ax_trq.set_xlabel("Time (s)")
    ax_trq.set_ylabel("Torque (N·m)")
    ax_trq.set_xlim(0, T_max * 1.05)
    ax_trq.grid(True, linestyle='--', alpha=0.2, color='#555588')
    ax_trq.axhline( tau_max, color='crimson', linestyle='--', lw=1.5, alpha=0.8,
                   label=f'Hard cap ±{tau_max} N·m')
    ax_trq.axhline(-tau_max, color='crimson', linestyle='--', lw=1.5, alpha=0.8)
    trq_dots = []
    for sc in results:
        slc = slice(0, sc['fail_frame'] + 1)
        ax_trq.plot(sc['t_grid'][slc], sc['tau'][0, slc],
                    '-',  color=sc['color'], lw=1.6, alpha=0.9)
        ax_trq.plot(sc['t_grid'][slc], sc['tau'][1, slc],
                    '--', color=sc['color'], lw=1.4, alpha=0.55)
        dot, = ax_trq.plot([], [], 'o', color=sc['color'], ms=8)
        trq_dots.append(dot)
    ax_trq.legend(fontsize=8, facecolor='#1a1a30',
                  edgecolor='#555588', labelcolor='white')

    plt.tight_layout(pad=1.5)

    # ---- Physical Time Synchronized Animation ----------------------------- #
    dt_anim = 0.04  # 40 ms per frame = 25 fps real-time playback
    dwell_time = 1.0  # pause 1s at completion before looping
    total_time = T_max + dwell_time
    total_frames = int(np.ceil(total_time / dt_anim))

    def update(frame):
        t_curr = frame * dt_anim
        t_display = min(t_curr, T_max)
        time_text.set_text(f"Time: {t_display:.2f} s / {T_max:.2f} s")

        artists = [time_text]
        for idx, sc in enumerate(results):
            if not sc['is_success']:
                t_end = sc['t_grid'][sc['fail_frame']]
            else:
                t_end = sc['T']

            # Evaluate state at physical time t_eval
            t_eval = min(t_curr, t_end)

            q1_t = np.interp(t_eval, sc['t_grid'], sc['q'][0])
            q2_t = np.interp(t_eval, sc['t_grid'], sc['q'][1])

            p0, p1, p2 = forward_kinematics(q1_t, q2_t)
            arm_lines[idx].set_data([p0[0], p1[0], p2[0]],
                                    [p0[1], p1[1], p2[1]])

            # Show failure marker if collided / violated constraint
            if not sc['is_success'] and t_curr >= t_end:
                fail_marks[idx].set_data([p2[0]], [p2[1]])
            else:
                fail_marks[idx].set_data([], [])

            # Interpolate state for time-series cursors
            v_curr   = np.interp(t_eval, sc['t_grid'], sc['v_ee'])
            dq1_curr = np.interp(t_eval, sc['t_grid'], sc['dq'][0])
            tau1_curr = np.interp(t_eval, sc['t_grid'], sc['tau'][0])

            ee_dots[idx].set_data( [t_eval], [v_curr])
            vel_dots[idx].set_data([t_eval], [dq1_curr])
            trq_dots[idx].set_data([t_eval], [tau1_curr])

            artists += [arm_lines[idx], fail_marks[idx],
                        ee_dots[idx], vel_dots[idx], trq_dots[idx]]
        return artists

    ani = FuncAnimation(fig, update, frames=total_frames,
                        interval=int(dt_anim * 1000), blit=False, repeat=True)
    plt.show()
    return ani


if __name__ == "__main__":
    pointA = np.array([ 1.2,  0.2])
    pointB = np.array([-0.6,  1.7])
    visualize_multi(pointA, pointB)
