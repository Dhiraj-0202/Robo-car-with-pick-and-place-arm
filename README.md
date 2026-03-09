Mobile Manipulator Robot Simulation 🤖

This project demonstrates a Mobile Manipulator System Simulation that combines a mobile robotic base and a two-link robotic arm capable of performing pick-and-place operations. The simulation is developed using Python and Pygame to visualize robot motion and test robotic arm control using Inverse Kinematics.

The system simulates the movement of a robotic arm mounted on a mobile base, allowing the robot to reach objects in the workspace, pick them using a gripper, and place them at designated locations.

Project Overview

Mobile manipulators are widely used in industrial automation, warehouses, and service robotics. This project focuses on understanding the core concepts behind such systems including:

Robot kinematics

Arm motion control

Object manipulation

Workspace visualization

A simulation environment was created to test the robot's movement and algorithms before implementing the hardware system.

Features

Mobile robot base movement

Two-link robotic arm model

Inverse Kinematics based arm control

Smooth servo-like arm motion

Gripper mechanism for object pickup

Pick-and-place object simulation

Workspace visualization

Real-time display of joint angles and end-effector position

Technologies Used

Python

Pygame

NumPy

Mathematics (Inverse Kinematics)

Working Principle

The robotic arm uses Inverse Kinematics to determine the joint angles required to reach a target position.

For a two-link robotic arm with link lengths 
𝐿
1
L
1
	​

 and 
𝐿
2
L
2
	​

, the joint angles are calculated using:

𝐷
=
𝑥
2
+
𝑦
2
−
𝐿
1
2
−
𝐿
2
2
2
𝐿
1
𝐿
2
D=
2L
1
	​

L
2
	​

x
2
+y
2
−L
1
2
	​

−L
2
2
	​

	​

𝜃
2
=
cos
⁡
−
1
(
𝐷
)
θ
2
	​

=cos
−1
(D)
𝜃
1
=
tan
⁡
−
1
(
𝑦
𝑥
)
−
tan
⁡
−
1
(
𝐿
2
sin
⁡
(
𝜃
2
)
𝐿
1
+
𝐿
2
cos
⁡
(
𝜃
2
)
)
θ
1
	​

=tan
−1
(
x
y
	​

)−tan
−1
(
L
1
	​

+L
2
	​

cos(θ
2
	​

)
L
2
	​

sin(θ
2
	​

)
	​

)

These angles control the movement of the robotic arm to reach the target object.

Controls
Key	Function
Arrow Keys	Move mobile base
P	Place object
Mouse / Target Logic	Arm moves toward object
Simulation Results

The robotic arm successfully reaches objects within its workspace.

Inverse kinematics correctly calculates joint angles.

The gripper picks and places objects within the simulation.

Smooth arm movement simulates real servo motor behavior.

Challenges Faced

Implementing accurate inverse kinematics calculations

Achieving smooth robotic arm movement

Handling object pickup logic

Coordinating arm movement with the mobile base

Maintaining simulation stability and performance

Future Improvements

Complete hardware implementation of the mobile manipulator

Integration with Arduino and servo motors

Wireless control using Bluetooth smartphone interface

Autonomous navigation and object detection

Obstacle avoidance
