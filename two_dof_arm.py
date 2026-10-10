import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import minimize

# --- Arm & Obstacle Parameters ---
l1, l2 = 1.0, 1.0  # Link lengths (m)
m1, m2 = 1.0, 1.0  # Link masses (kg)

# Joint Torque Limit Parameter (Hard Constraint)
tau_max = 20.0     # Hard maximum allowed joint torque (N·m)

# Khatib (1986) Obstacle Parameters
p_obs = np.array([0.8, 1.0])  # Obstacle center position (m)
r_obs = 0.25                  # Physical radius of obstacle (m)
rho_0 = 0.35                  # Distance of influence (m)
eta_rep = 1.0                # Khatib repulsive potential gain
w_vel_pot = 1000              # Kinetic-Potential coupling weight (slow down inside potential field)

def forward_kinematics(q1, q2):
    """Returns Cartesian coordinates of (Base, Joint 1, End-Effector)."""
    x1, y1 = l1 * np.cos(q1), l1 * np.sin(q1)
    x2, y2 = x1 + l2 * np.cos(q1 + q2), y1 + l2 * np.sin(q1 + q2)
    return np.array([0.0, 0.0]), np.array([x1, y1]), np.array([x2, y2])

def inverse_kinematics(x, y):
    """Computes joint angles [q1, q2] for Cartesian target (x, y)."""
    r2 = x**2 + y**2
    cos_q2 = np.clip((r2 - l1**2 - l2**2) / (2 * l1 * l2), -0.999, 0.999)
    q2 = np.arccos(cos_q2)
    q1 = np.arctan2(y, x) - np.arctan2(l2 * np.sin(q2), l1 + l2 * np.cos(q2))
    return np.array([q1, q2])

def compute_dynamics(q, dq, d2q):
    """Computes required joint torques [tau1, tau2] given state and acceleration."""
    q1, q2 = q[0], q[1]
    dq1, dq2 = dq[0], dq[1]
    d2q1, d2q2 = d2q[0], d2q[1]
    
    lc1, lc2 = l1 / 2.0, l2 / 2.0
    I1, I2 = m1 * l1**2 / 12.0, m2 * l2**2 / 12.0
    
    # Mass matrix M(q)
    M11 = m1 * lc1**2 + I1 + m2 * (l1**2 + lc2**2 + 2 * l1 * lc2 * np.cos(q2)) + I2
    M12 = m2 * (lc2**2 + l1 * lc2 * np.cos(q2)) + I2
    M22 = m2 * lc2**2 + I2
    
    # Coriolis/Centrifugal & Gravity terms
    h = -m2 * l1 * lc2 * np.sin(q2)
    C1 = h * dq2 * dq1 + h * (dq1 + dq2) * dq2
    C2 = -h * dq1**2
    
    g1 = (m1 * lc1 + m2 * l1) * 9.81 * np.cos(q1) + m2 * lc2 * 9.81 * np.cos(q1 + q2)
    g2 = m2 * lc2 * 9.81 * np.cos(q1 + q2)
    
    tau1 = M11 * d2q1 + M12 * d2q2 + C1 + g1
    tau2 = M12 * d2q1 + M22 * d2q2 + C2 + g2
    return np.array([tau1, tau2])

def end_effector_repulsive_potential(ee_pos):
    """
    Computes Khatib (1986) Repulsive Potential U_rep(p) for the End-Effector:
    U_rep(p) = 0.5 * eta * (1/rho - 1/rho_0)^2  if rho <= rho_0 else 0
    where rho is shortest distance from end-effector to the obstacle surface.
    """
    dist = np.linalg.norm(ee_pos - p_obs) - r_obs
    effective_dist = max(dist, 1e-4)
    
    if dist <= rho_0:
        u = 0.5 * eta_rep * ((1.0 / effective_dist) - (1.0 / rho_0))**2
        if dist < 1e-4:
            # Steep linear gradient pushing OUT of obstacle
            u += 1e5 * (1e-4 - dist)
        return u
    return 0.0

def check_end_effector_collision(ee_pos):
    """Collision is defined strictly as contact between the end-effector and the obstacle."""
    return np.linalg.norm(ee_pos - p_obs) <= r_obs

def get_trajectory(params, qA, qB, N=100, K=4):
    """Generates trajectory [T, t, q, dq, tau] parameterized by time T and shape coefficients."""
    T = params[0]
    c1 = params[1 : 1 + K]
    c2 = params[1 + K : 1 + 2 * K]
    
    s = np.linspace(0, 1, N)
    s2, s3, s4, s5 = s**2, s**3, s**4, s**5
    
    # Base quintic trajectory ensuring zero boundary velocity
    q_base = 10 * s3 - 15 * s4 + 6 * s5
    dq_base = 30 * s2 - 60 * s3 + 30 * s4
    
    q1 = qA[0] + (qB[0] - qA[0]) * q_base
    q2 = qA[1] + (qB[1] - qA[1]) * q_base
    dq1 = (qB[0] - qA[0]) * dq_base / T
    dq2 = (qB[1] - qA[1]) * dq_base / T
    
    # Add K smooth basis modes: b_k(s) = s^(k+3) * (1-s)^3
    for k in range(K):
        p_val = k + 3
        b = s**p_val * (1 - s)**3
        db = p_val * s**(p_val - 1) * (1 - s)**3 - 3 * s**p_val * (1 - s)**2
        
        q1 += c1[k] * b
        q2 += c2[k] * b
        dq1 += c1[k] * db / T
        dq2 += c2[k] * db / T
    
    t_grid = s * T
    d2q1 = np.gradient(dq1, t_grid)
    d2q2 = np.gradient(dq2, t_grid)
    
    q = np.vstack([q1, q2])
    dq = np.vstack([dq1, dq2])
    d2q = np.vstack([d2q1, d2q2])
    
    tau = np.zeros_like(q)
    for i in range(N):
        tau[:, i] = compute_dynamics(q[:, i], dq[:, i], d2q[:, i])
        
    return T, t_grid, q, dq, tau

def optimize_trajectory(pA, pB, K=4, max_retries=6):
    """
    Optimizes trajectory minimizing duration T, total torque effort (integral tau^2 dt),
    and a Kinetic-Potential Coupling penalty (U_rep * ||v_EE||^2) that forces the arm to slow down inside the potential field.
    Enforces HARD INEQUALITY CONSTRAINTS for joint torque limits (|tau_i| <= tau_max).
    """
    qA = inverse_kinematics(pA[0], pA[1])
    qB = inverse_kinematics(pB[0], pB[1])
    
    # 1. Objective Function (Time + Torque Effort + Repulsive Potential + Potential-Velocity Coupling)
    def cost_func(x):
        T, t, q, dq, tau = get_trajectory(x, qA, qB, N=40, K=K)
        dt = T / 39.0
        effort = np.sum(tau**2) * dt
        
        u_rep = 0.0
        vel_pot_coupling = 0.0
        
        # Calculate end-effector positions & velocities
        ee_positions = [forward_kinematics(q[0, i], q[1, i])[2] for i in range(len(t))]
        
        for i in range(len(t)):
            u = end_effector_repulsive_potential(ee_positions[i])
            u_rep += u * dt
            
            # Estimate end-effector speed magnitude ||v_EE||
            if 0 < i < len(t) - 1:
                v_ee = (ee_positions[i + 1] - ee_positions[i - 1]) / (2.0 * dt)
                v_ee_sq = np.sum(v_ee**2)
                # Kinetic-Potential Coupling: Penalize high speed inside high potential fields
                vel_pot_coupling += u * v_ee_sq * dt
            
        return 1.5 * T + 0.05 * effort + u_rep + w_vel_pot * vel_pot_coupling

    # 2. Hard Inequality Constraints: |tau_1(t)| <= tau_max and |tau_2(t)| <= tau_max (must be >= 0)
    def torque_hard_constraint(x):
        T, t, q, dq, tau = get_trajectory(x, qA, qB, N=25, K=K)
        c1 = tau_max - np.abs(tau[0])
        c2 = tau_max - np.abs(tau[1])
        return np.hstack([c1, c2])

    bounds = [(0.2, 10.0)] + [(-15, 15)] * (2 * K)
    constraints = [{'type': 'ineq', 'fun': torque_hard_constraint}]
    
    # Generate multi-start initial guesses
    initial_guesses = [
        [1.5] + [0.0] * (2 * K),
        [2.5] + [0.0] * (2 * K),
        [3.5] + [0.0] * (2 * K),
    ]
    
    np.random.seed(42)
    for _ in range(max_retries - len(initial_guesses)):
        t_guess = np.random.uniform(1.8, 4.0)
        c_guess = list(np.random.uniform(-3.0, 3.0, 2 * K))
        initial_guesses.append([t_guess] + c_guess)

    best_result = None
    best_cost = float('inf')

    for attempt_idx, x0 in enumerate(initial_guesses):
        res = minimize(cost_func, x0, bounds=bounds, constraints=constraints, method='SLSQP')
        T, t_grid, q, dq, tau = get_trajectory(res.x, qA, qB, N=100, K=K)
        
        # Check collision and hard torque bounds
        has_collision = False
        fail_frame = len(t_grid) - 1
        for i in range(len(t_grid)):
            _, _, ee_pos = forward_kinematics(q[0, i], q[1, i])
            if check_end_effector_collision(ee_pos):
                has_collision = True
                fail_frame = i
                break
                
        max_tau_val = np.max(np.abs(tau))
        torque_exceeded = max_tau_val > (tau_max + 0.1)
        
        is_success = res.success and not has_collision and not torque_exceeded
        
        if is_success:
            current_cost = cost_func(res.x)
            if current_cost < best_cost:
                best_cost = current_cost
                best_result = (T, t_grid, q, dq, tau, True, fail_frame, attempt_idx + 1)
                break
                
        if best_result is None:
            best_result = (T, t_grid, q, dq, tau, False, fail_frame, attempt_idx + 1)

    return best_result

def visualize(pA, pB):
    """Visualizes 2D arm motion, velocity modulation inside potential fields, and dynamics plots."""
    T, t_grid, q, dq, tau, is_success, fail_frame, attempts = optimize_trajectory(pA, pB)
    
    dt = T / (len(t_grid) - 1)
    total_effort = np.sum(tau**2) * dt
    max_tau_reached = np.max(np.abs(tau))

    if not is_success:
        print(f"\n[OPTIMIZATION FAILED] Tested {attempts} attempts, but no solution satisfying hard torque limits (±{tau_max} N·m) and obstacle clearance was found!")
        print(f"End-effector collides or violates hard constraints at t = {t_grid[fail_frame]:.2f} s\n")
    else:
        print(f"\n[OPTIMIZATION SUCCESS] Potential-Field Velocity Modulation Trajectory Found on Attempt #{attempts}!")
        print(f"  • Duration (T): {T:.2f} s")
        print(f"  • Integrated Torque Effort (∫||τ||² dt): {total_effort:.1f} N²·m²·s")
        print(f"  • Max Joint Torque Reached: {max_tau_reached:.1f} N·m (Hard Cap: ±{tau_max} N·m)\n")

    # Compute End-Effector position and velocity over time
    ee_x = np.zeros(len(t_grid))
    ee_y = np.zeros(len(t_grid))
    for i in range(len(t_grid)):
        _, _, p2 = forward_kinematics(q[0, i], q[1, i])
        ee_x[i], ee_y[i] = p2[0], p2[1]

    vx = np.gradient(ee_x, t_grid)
    vy = np.gradient(ee_y, t_grid)
    v_ee = np.hypot(vx, vy)  # End-effector speed magnitude (m/s)

    # Setup 4 subplots
    fig = plt.figure(figsize=(13, 7))
    ax_arm = plt.subplot(3, 2, (1, 5))
    ax_ee_vel = plt.subplot(3, 2, 2)
    ax_vel = plt.subplot(3, 2, 4)
    ax_trq = plt.subplot(3, 2, 6)

    # 1. 2D Arm Workspace Setup
    reach = l1 + l2 + 0.2
    ax_arm.set_xlim(-reach, reach)
    ax_arm.set_ylim(-reach, reach)
    ax_arm.set_aspect('equal')
    ax_arm.grid(True, linestyle='--', alpha=0.5)
    
    if is_success:
        title_text = f"2-DOF Arm Motion (Attempt #{attempts}, T={T:.2f}s, Velocity Modulated in APF) - SUCCESS"
        title_color = 'darkgreen'
    else:
        title_text = f"FAILED: Constraint Violation at t = {t_grid[fail_frame]:.2f} s"
        title_color = 'crimson'
        
    ax_arm.set_title(title_text, color=title_color, fontweight='bold', fontsize=11)
    
    # Plot Start, Target, Path up to collision frame
    ax_arm.plot(pA[0], pA[1], 'go', markersize=10, label='Start A')
    ax_arm.plot(pB[0], pB[1], 'ro', markersize=10, label='Target B')
    
    valid_slice = slice(0, fail_frame + 1)
    ax_arm.plot(ee_x[valid_slice], ee_y[valid_slice], 'k--', alpha=0.5, label='EE Path')
    
    # Draw Khatib Obstacle and Influence Zone (rho_0)
    obs_color = 'crimson' if not is_success else 'darkred'
    obs_circle = plt.Circle(p_obs, r_obs, color=obs_color, alpha=0.85, label='Obstacle')
    inf_circle = plt.Circle(p_obs, r_obs + rho_0, color='orange', linestyle='--', fill=False, lw=1.5, label=r'Khatib Potential Region ($\rho_0$)')
    ax_arm.add_patch(obs_circle)
    ax_arm.add_patch(inf_circle)
    
    (arm_line,) = ax_arm.plot([], [], 'o-', lw=4, ms=8, color='deepskyblue')
    (collision_marker,) = ax_arm.plot([], [], 'rX', markersize=14, markeredgewidth=3, label='Collision!')
    ax_arm.legend(loc='lower left')

    # 2. End-Effector Velocity Plot (Highlighting velocity drop inside APF)
    ax_ee_vel.plot(t_grid[valid_slice], v_ee[valid_slice], label=r'Speed $\|v_{EE}\|$ (Modulated in APF)', color='tab:green', lw=2)
    ax_ee_vel.set_title("End-Effector Velocity over Time (Slowing down in APF)")
    ax_ee_vel.set_ylabel("Speed (m/s)")
    ax_ee_vel.grid(True, linestyle='--', alpha=0.5)
    ax_ee_vel.legend(loc='upper right')
    (cur_ee_vel,) = ax_ee_vel.plot([], [], 'ro')

    # 3. Joint Velocity Plot
    ax_vel.plot(t_grid[valid_slice], dq[0, valid_slice], label=r'$\dot{\theta}_1$ (Joint 1)', color='tab:blue')
    ax_vel.plot(t_grid[valid_slice], dq[1, valid_slice], label=r'$\dot{\theta}_2$ (Joint 2)', color='tab:orange')
    ax_vel.set_title("Joint Velocities over Time")
    ax_vel.set_ylabel("Velocity (rad/s)")
    ax_vel.grid(True, linestyle='--', alpha=0.5)
    ax_vel.legend(loc='upper right')
    (cur_vel,) = ax_vel.plot([], [], 'ro')

    # 4. Joint Torque Plot with Hard Torque Limit Lines
    ax_trq.plot(t_grid[valid_slice], tau[0, valid_slice], label=r'$\tau_1$ (Joint 1)', color='tab:blue')
    ax_trq.plot(t_grid[valid_slice], tau[1, valid_slice], label=r'$\tau_2$ (Joint 2)', color='tab:orange')
    
    # Draw horizontal Hard Torque Limit lines
    ax_trq.axhline(tau_max, color='red', linestyle='--', lw=1.5, label=f'Hard Torque Limit (±{tau_max} N·m)')
    ax_trq.axhline(-tau_max, color='red', linestyle='--', lw=1.5)
    
    ax_trq.set_title("Joint Torques over Time (Strict Hard Limit Enforced)", fontsize=11)
    ax_trq.set_xlabel("Time (s)")
    ax_trq.set_ylabel("Torque (N·m)")
    ax_trq.grid(True, linestyle='--', alpha=0.5)
    ax_trq.legend(loc='upper right', fontsize=8)
    (cur_trq,) = ax_trq.plot([], [], 'ro')

    plt.tight_layout()

    num_anim_frames = fail_frame + 1

    def update(frame):
        p0, p1, p2 = forward_kinematics(q[0, frame], q[1, frame])
        arm_line.set_data([p0[0], p1[0], p2[0]], [p0[1], p1[1], p2[1]])
        cur_ee_vel.set_data([t_grid[frame]], [v_ee[frame]])
        cur_vel.set_data([t_grid[frame]], [dq[0, frame]])
        cur_trq.set_data([t_grid[frame]], [tau[0, frame]])
        
        if not is_success and frame == fail_frame:
            collision_marker.set_data([p2[0]], [p2[1]])
        else:
            collision_marker.set_data([], [])
            
        return arm_line, cur_ee_vel, cur_vel, cur_trq, collision_marker

    ani = FuncAnimation(fig, update, frames=num_anim_frames, interval=T * 1000 / len(t_grid), repeat=True)
    plt.show()
    return ani

if __name__ == "__main__":
    pointA = np.array([1.2, 0.2])
    pointB = np.array([-0.6, 1.7])
    visualize(pointA, pointB)