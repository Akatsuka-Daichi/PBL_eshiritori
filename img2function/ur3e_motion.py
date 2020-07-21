
import sys
import copy
import rospy
import math
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import numpy as np
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from moveit_msgs.msg import PlanningScene, ObjectColor

from scipy.spatial.transform import Rotation
## END_SUB_TUTORIAL

def all_close(goal, actual, tolerance):
  """
  Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
  @param: goal       A list of floats, a Pose or a PoseStamped
  @param: actual     A list of floats, a Pose or a PoseStamped
  @param: tolerance  A float
  @returns: bool
  """
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True

class MoveGroupPythonIntefaceTutorial(object):
  """MoveGroupPythonIntefaceTutorial"""
  def __init__(self):
    super(MoveGroupPythonIntefaceTutorial, self).__init__()

    ## BEGIN_SUB_TUTORIAL setup
    ##
    ## First initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial',
                    anonymous=True)

    ## Instantiate a `RobotCommander`_ object. This object is the outer-level interface to
    ## the robot:
    robot = moveit_commander.RobotCommander()

    ## Instantiate a `PlanningSceneInterface`_ object.  This object is an interface
    ## to the world surrounding the robot:
    scene = moveit_commander.PlanningSceneInterface()

    ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
    ## to one group of joints.  In this case the group is the joints in the Panda
    ## arm so we set ``group_name = panda_arm``. If you are using a different robot,
    ## you should change this value to the name of your robot arm planning group.
    ## This interface can be used to plan and execute motions on the Panda:
    group_name = "manipulator"
    group = moveit_commander.MoveGroupCommander(group_name)

    ## We create a `DisplayTrajectory`_ publisher which is used later to publish
    ## trajectories for RViz to visualize:
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    ## END_SUB_TUTORIAL

    ## BEGIN_SUB_TUTORIAL basic_info
    ##
    ## Getting Basic Information
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^
    # We can get the name of the reference frame for this robot:
    planning_frame = group.get_planning_frame()
    print "============ Reference frame: %s" % planning_frame

    # We can also print the name of the end-effector link for this group:
    eef_link = group.get_end_effector_link()
    print "============ End effector: %s" % eef_link

    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print "============ Robot Groups:", robot.get_group_names()

    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""
    ## END_SUB_TUTORIAL

    # Misc variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.group = group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names

  def go_to_joint_initialstate1(self):
    group = self.group

    ## 各角度を指定する
    joint_goal = group.get_current_joint_values()
    joint_goal[0] = 0#nemoto
    joint_goal[1] = -pi/2#2
    joint_goal[2] = 0#3
    joint_goal[3] = -pi/2#4
    joint_goal[4] = 0#5
    joint_goal[5] = 0#6

    (plan) = group.plan(joint_goal)

    return plan
  
  def go_to_joint_initialstate2(self):
    group = self.group

    joint_goal = group.get_current_joint_values()
    joint_goal[0] = 0#nemoto
    joint_goal[1] = math.radians(-80)#2
    joint_goal[2] = 0#3
    joint_goal[3] = -pi/2#4
    joint_goal[4] = 0#5
    joint_goal[5] = 0#6

    (plan) = group.plan(joint_goal)

    return plan
  
  def go_to_joint_initialstate3(self):
    group = self.group

    joint_goal = group.get_current_joint_values()
    joint_goal[0] = 0#nemoto
    joint_goal[1] = math.radians(-80)#2
    joint_goal[2] = math.radians(100)#3
    joint_goal[3] = -pi/2#4
    joint_goal[4] = 0#5
    joint_goal[5] = 0#6

    (plan) = group.plan(joint_goal)

    return plan
  
  def go_to_joint_initialstate4(self):
    group = self.group

    joint_goal = group.get_current_joint_values()
    joint_goal[0] = 0#nemoto
    joint_goal[1] = math.radians(-80)#2
    joint_goal[2] = math.radians(100)#3
    joint_goal[3] = math.radians(-110)#4
    joint_goal[4] = 0#5
    joint_goal[5] = 0#6
    
    (plan) = group.plan(joint_goal)

    return plan

  def go_to_joint_initialstate5(self):
    group = self.group

    joint_goal = group.get_current_joint_values()
    joint_goal[0] = 0#nemoto
    joint_goal[1] = math.radians(-80)#2
    joint_goal[2] = math.radians(100)#3
    joint_goal[3] = math.radians(-110)#4
    joint_goal[4] = math.radians(-90)#5
    joint_goal[5] = 0#6
    
    (plan) = group.plan(joint_goal)

    return plan

  def go_to_joint_initialstate6(self):
      group = self.group

      joint_goal = group.get_current_joint_values()
      joint_goal[0] = 0#nemoto
      joint_goal[1] = math.radians(-80)#2
      joint_goal[2] = math.radians(100)#3
      joint_goal[3] = math.radians(-110)#4
      joint_goal[4] = math.radians(-90)#5
      joint_goal[5] = 0#6
      
      (plan) = group.plan(joint_goal)

      return plan


  def plan_touching_start_point(self,file):
    group = self.group

    data = np.loadtxt(file,                                             # 読み込みたいファイルのパス
                      delimiter=",",                                    # ファイルの区切り文字
                      skiprows=0,                                       # 先頭の何行を無視するか（指定した行数までは読み込まない）
                      usecols=(0,1,2,3,4,5,6)                           # 読み込みたい列番号
                     )
    size = data.shape
    waypoints = []

    #現在の位置を格納
    wpose = group.get_current_pose().pose
    startposition = wpose

    #realsensedata.csvに格納されているはじめの行を読み取る
    #格納データは[0 1 2 3 4 5 6] = [eulerZ eulerY eulerZ 0 Xposition Yposition Zposition]
    i =0
    eulerZ = data[i,0]
    eulerY = data[i,1]
    eulerZZ = data[i,2]

    sx = data[i,4]
    sy = data[i,5]
    sz = data[i,6]

    #オイラー角をクォータニオン(q)に変換
    euler = np.zeros(3)
    euler[0] = eulerZ
    euler[1] = eulerY
    euler[2] = eulerZZ
    rot = Rotation.from_euler('zyz',euler,degrees=True)
    q = rot.as_quat()

    #qに格納された[x y z w]をそれぞれwpose.orientationに格納
    wpose.orientation.w = q[3]
    wpose.orientation.x = q[0]
    wpose.orientation.y = q[1]
    wpose.orientation.z = q[2]

    #realsensedata.csvに格納されている[Xposition Yposition Zposition]をそれぞれwpose.positionに格納
    wpose.position.x = -sx+0.05
    wpose.position.y = -sy
    wpose.position.z = sz

    #wposeデータを一式waypointに格納
    waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    # 動作計画を行う
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold
    # Note: We are just planning, not asking move_group to actually move the robot yet:


    #動作スピードコントロール,動作速度要因0-1の間で調整
    print "============ Press `Enter` 撫で動作の再動作計画 ..."
    raw_input()
    robot = moveit_commander.RobotCommander()
    robot_state = robot.get_current_state()
    plan2 = group.retime_trajectory(robot_state, plan, velocity_scaling_factor = 0.01)

    return plan2, fraction

  def plan_touching_motion(self,file):
    group = self.group

    data = np.loadtxt(file,                                             # 読み込みたいファイルのパス
                      delimiter=",",                                    # ファイルの区切り文字
                      skiprows=0,                                       # 先頭の何行を無視するか（指定した行数までは読み込まない）
                      usecols=(0,1,2,3,4,5,6)                           # 読み込みたい列番号
                     )
    size = data.shape

    waypoints = []

    #現在の位置を格納
    wpose = group.get_current_pose().pose
    startposition = wpose


    euler = np.zeros(3)
    for i in range(0,size[0]):
       #realsensedata.csvに格納されているi番目の行を読み取る
       #格納データは[0 1 2 3 4 5 6] = [eulerZ eulerY eulerZZ 0 Xposition Yposition Zposition]
        eulerZ = data[i,0]
        eulerY = data[i,1]
        eulerZZ = data[i,2]

        sx = data[i,4]
        sy = data[i,5]
        sz = data[i,6]

        euler = np.zeros(3)
        euler[0] = eulerZ
        euler[1] = eulerY
        euler[2] = eulerZZ

        #オイラー角をクォータニオン(q)に変換
        rot = Rotation.from_euler('zyz',euler,degrees=True)
        q = rot.as_quat()

        #qに格納された[x y z w]をそれぞれwpose.orientationに格納
        wpose.orientation.w = q[3]
        wpose.orientation.x = q[0]
        wpose.orientation.y = q[1]
        wpose.orientation.z = q[2]


        #realsensedata.csvに格納されている[Xposition Yposition Zposition]をそれぞれwpose.positionに格納
        wpose.position.x = -sx+0.05
        wpose.position.y = -sy
        wpose.position.z = sz

        #wposeデータを一式waypointに格納
        waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    # 動作計画を行う 	
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.001,        # eef_step
                                       0.0)         # jump_threshold	


    #動作スピードコントロール,動作速度要因0-1の間で調整
    print "============ Press `Enter` 撫で動作の再動作計画 ..."
    raw_input()
    robot = moveit_commander.RobotCommander()
    robot_state = robot.get_current_state()
    plan2 = group.retime_trajectory(robot_state, plan, velocity_scaling_factor = 0.01)
    # Note: We are just planning, not asking move_group to actually move the robot yet:

    return plan2, fraction


  def plan_touching_motion2(self,file):
    group = self.group

    data = np.loadtxt(file,                                             # 読み込みたいファイルのパス
                      delimiter=",",                                    # ファイルの区切り文字
                      skiprows=0,                                       # 先頭の何行を無視するか（指定した行数までは読み込まない）
                      usecols=(0,1,2,3,4,5,6)                           # 読み込みたい列番号
                     )
    size = data.shape

    waypoints = []

    #現在の位置を格納
    wpose = group.get_current_pose().pose
    startposition = wpose
    print(startposition)

   

    sx = 0.29
    sy = -0.108
    sz = 0.047

    for i in range(0,1):
      euler = np.zeros(3)
      
      eulerZ = data[i,0]
      eulerY = data[i,1]
      eulerZZ = data[i,2]

      sx = data[i,4]
      sy = data[i,5]
      sz = data[i,6]

      euler[0] = eulerZ
      euler[1] = eulerY
      euler[2] = eulerZZ
      #オイラー角をクォータニオン(q)に変換
      rot = Rotation.from_euler('zyz',euler,degrees=True)
      q = rot.as_quat()
      # qに格納された[x y z w]をそれぞれwpose.orientationに格納
      wpose.orientation.w = q[3]
      wpose.orientation.x = q[0]
      wpose.orientation.y = q[1]
      wpose.orientation.z = q[2]

      #realsensedata.csvに格納されている[Xposition Yposition Zposition]をそれぞれwpose.positionに格納
      wpose.position.x = sx
      wpose.position.y = sy
      wpose.position.z = sz

      #wposeデータを一式waypointに格納
      waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    # 動作計画を行う 	
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.001,        # eef_step
                                       0.0)         # jump_threshold	


    #動作スピードコントロール,動作速度要因0-1の間で調整
    print "============ Press `Enter` 撫で動作の再動作計画 ..."
    raw_input()
    robot = moveit_commander.RobotCommander()
    robot_state = robot.get_current_state()
    plan2 = group.retime_trajectory(robot_state, plan, velocity_scaling_factor = 0.01)
    # Note: We are just planning, not asking move_group to actually move the robot yet:

   
    return plan2, fraction


  def plan_touching_motion3(self,file):
    group = self.group

    data = np.loadtxt(file,                                             # 読み込みたいファイルのパス
                      delimiter=",",                                    # ファイルの区切り文字
                      skiprows=0,                                       # 先頭の何行を無視するか（指定した行数までは読み込まない）
                      usecols=(0,1,2,3,4,5,6)                           # 読み込みたい列番号
                      )
    size = data.shape

    waypoints = []

    #現在の位置を格納
    wpose = group.get_current_pose().pose
    startposition = wpose
    print(startposition)

    

    sx = 0.29
    sy = -0.108
    sz = 0.047

    for i in range(0,size[0]-1):
      euler = np.zeros(3)
      
      eulerZ = data[i,0]
      eulerY = data[i,1]
      eulerZZ = data[i,2]

      sx = data[i,4]
      sy = data[i,5]
      sz = data[i,6]

      euler[0] = eulerZ
      euler[1] = eulerY
      euler[2] = eulerZZ
      #オイラー角をクォータニオン(q)に変換
      rot = Rotation.from_euler('zyz',euler,degrees=True)
      q = rot.as_quat()
      # qに格納された[x y z w]をそれぞれwpose.orientationに格納
      wpose.orientation.w = q[3]
      wpose.orientation.x = q[0]
      wpose.orientation.y = q[1]
      wpose.orientation.z = q[2]

      #realsensedata.csvに格納されている[Xposition Yposition Zposition]をそれぞれwpose.positionに格納
      wpose.position.x = sx
      wpose.position.y = sy
      wpose.position.z = sz

      #wposeデータを一式waypointに格納
      waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    # 動作計画を行う 	
    (plan, fraction) = group.compute_cartesian_path(
                                        waypoints,   # waypoints to follow
                                        0.001,        # eef_step
                                        0.0)         # jump_threshold	


    #動作スピードコントロール,動作速度要因0-1の間で調整
    print "============ Press `Enter` 撫で動作の再動作計画 ..."
    raw_input()
    robot = moveit_commander.RobotCommander()
    robot_state = robot.get_current_state()
    plan2 = group.retime_trajectory(robot_state, plan, velocity_scaling_factor = 0.01)
    # Note: We are just planning, not asking move_group to actually move the robot yet:

    
    return plan2, fraction

  def plan_touching_motion4(self,file):
    group = self.group

    data = np.loadtxt(file,                                             # 読み込みたいファイルのパス
                      delimiter=",",                                    # ファイルの区切り文字
                      skiprows=0,                                       # 先頭の何行を無視するか（指定した行数までは読み込まない）
                      usecols=(0,1,2,3,4,5,6)                           # 読み込みたい列番号
                      )
    size = data.shape

    waypoints = []

    #現在の位置を格納
    wpose = group.get_current_pose().pose
    startposition = wpose
    print(startposition)

    

    sx = 0.29
    sy = -0.108
    sz = 0.047

    for i in range(size[0]-1,size[0]):
      euler = np.zeros(3)
      
      eulerZ = data[i,0]
      eulerY = data[i,1]
      eulerZZ = data[i,2]

      sx = data[i,4]
      sy = data[i,5]
      sz = data[i,6]

      euler[0] = eulerZ
      euler[1] = eulerY
      euler[2] = eulerZZ
      #オイラー角をクォータニオン(q)に変換
      rot = Rotation.from_euler('zyz',euler,degrees=True)
      q = rot.as_quat()
      # qに格納された[x y z w]をそれぞれwpose.orientationに格納
      wpose.orientation.w = q[3]
      wpose.orientation.x = q[0]
      wpose.orientation.y = q[1]
      wpose.orientation.z = q[2]

      #realsensedata.csvに格納されている[Xposition Yposition Zposition]をそれぞれwpose.positionに格納
      wpose.position.x = sx
      wpose.position.y = sy
      wpose.position.z = sz

      #wposeデータを一式waypointに格納
      waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    # 動作計画を行う 	
    (plan, fraction) = group.compute_cartesian_path(
                                        waypoints,   # waypoints to follow
                                        0.001,        # eef_step
                                        0.0)         # jump_threshold	


    #動作スピードコントロール,動作速度要因0-1の間で調整
    print "============ Press `Enter` 撫で動作の再動作計画 ..."
    raw_input()
    robot = moveit_commander.RobotCommander()
    robot_state = robot.get_current_state()
    plan2 = group.retime_trajectory(robot_state, plan, velocity_scaling_factor = 0.01)
    # Note: We are just planning, not asking move_group to actually move the robot yet:

    
    return plan2, fraction


  def execute_plan(self, plan):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group
    ## BEGIN_SUB_TUTORIAL execute_plan
    ##
    ## Executing a Plan
    ## ^^^^^^^^^^^^^^^^
    ## Use execute if you would like the robot to follow
    ## the plan that has already been computed:
    group.execute(plan, wait=True)

    ## **Note:** The robot's current joint state must be within some tolerance of the
    ## first waypoint in the `RobotTrajectory`_ or ``execute()`` will fail
    ## END_SUB_TUTORIAL

def main():
  #順々に動作させ，初期位置に移動させる場合は"1"
  #その他は一度に初期位置に移動
  flag = 1

  #ファイルが格納されたパスを指定
  filepath = "/home/akatsuka/catkin_ws/src/ur3e_motion_practice/src/cat_best_order.csv"

  try:
    print "============ Press `Enter` プログラム開始(press ctrl-d to exit) ..."
    raw_input()
    tutorial = MoveGroupPythonIntefaceTutorial()

    if flag == 1:
      print "============ Press `Enter` 初期位置の動作計画(1/5) ..."
      raw_input()
      cartesian_plan = tutorial.go_to_joint_initialstate1()
      print "============ Press `Enter` 動作実行(1/5) ..."
      raw_input()
      tutorial.execute_plan(cartesian_plan)

      print "============ Press `Enter` 初期位置の動作計画(2/5) ..."
      raw_input()
      cartesian_plan = tutorial.go_to_joint_initialstate2()
      print "============ Press `Enter` 動作実行(2/5) ..."
      raw_input()
      tutorial.execute_plan(cartesian_plan)

      print "============ Press `Enter` 初期位置の動作計画(3/5) ..."
      raw_input()
      cartesian_plan = tutorial.go_to_joint_initialstate3()
      print "============ Press `Enter` 動作実行(3/5) ..."
      raw_input()
      tutorial.execute_plan(cartesian_plan)

      print "============ Press `Enter` 初期位置の動作計画(4/5) ..."
      raw_input()
      cartesian_plan = tutorial.go_to_joint_initialstate4()
      print "============ Press `Enter` 動作実行(4/5) ..."
      raw_input()
      tutorial.execute_plan(cartesian_plan)
      print "============ Press `Enter` 初期位置の動作計画(5-1/5)待ち状態 ..."
      raw_input()
      cartesian_plan = tutorial.go_to_joint_initialstate5()
      print "============ Press `Enter` 動作実行(5-1/5) ..."
      raw_input()
      tutorial.execute_plan(cartesian_plan)
      print "============ Press `Enter` 初期位置の動作計画(5-2/5)IK解き直し ..."
      raw_input()
      cartesian_plan = tutorial.go_to_joint_initialstate5()
      print "============ Press `Enter` 動作実行(5-2/5) ..."
      raw_input()
      tutorial.execute_plan(cartesian_plan)
      # print "============ Press `Enter` 初期位置の動作計画(6/4) ..."
      # raw_input()
      # cartesian_plan = tutorial.go_to_joint_initialstate6()
      # print "============ Press `Enter` 動作実行(6/4) ..."
      # raw_input()
      # tutorial.execute_plan(cartesian_plan)
    else:
      print "============ Press `Enter` 初期位置の動作計画 ..."
      raw_input()
      cartesian_plan = tutorial.go_to_joint_initialstate6()
      print "============ Press `Enter` 動作実行 ..."
      raw_input()
      tutorial.execute_plan(cartesian_plan)



    # print "============ Press `Enter` 動作開始位置に移動する動作計画 ..."
    # raw_input()
    # cartesian_plan, fraction = tutorial.plan_touching_start_point(filepath)
    # print "============ Press `Enter` 動作開始位置に移動 ..."
    # raw_input()
    # tutorial.execute_plan(cartesian_plan)


    print "============ Press `Enter` 撫で動作の動作計画(stay position) ..."
    raw_input()
    cartesian_plan, fraction = tutorial.plan_touching_motion2(filepath)
    print "============ Press `Enter` 撫で動作実行(stay position) ..."
    raw_input()
    tutorial.execute_plan(cartesian_plan)

    print "============ Press `Enter` 撫で動作の動作計画(stay position解き直し) ..."
    raw_input()
    cartesian_plan, fraction = tutorial.plan_touching_motion2(filepath)
    print "============ Press `Enter` 撫で動作実行(stay position解き直し) ..."
    raw_input()
    tutorial.execute_plan(cartesian_plan)

    print "============ Press `Enter` 撫で動作の動作計画 ..."
    raw_input()
    cartesian_plan, fraction = tutorial.plan_touching_motion3(filepath)
    print "============ Press `Enter` 撫で動作実行 ..."
    raw_input()
    tutorial.execute_plan(cartesian_plan)

    print "============ Press `Enter` 撫で動作の動作計画 ..."
    raw_input()
    cartesian_plan, fraction = tutorial.plan_touching_motion4(filepath)
    print "============ Press `Enter` 撫で動作実行 ..."
    raw_input()
    tutorial.execute_plan(cartesian_plan)
    
    
    
    print "============ Press `Enter` 初期位置の動作計画(5/4) ..."
    raw_input()
    cartesian_plan = tutorial.go_to_joint_initialstate5()
    print "============ Press `Enter` 動作実行(5/4) ..."
    raw_input()
    tutorial.execute_plan(cartesian_plan)
    
    # print "============ Press `Enter` 初期位置に戻る動作計画 ..."
    # raw_input()
    # cartesian_plan = tutorial.go_to_joint_initialstate4()
    # print "============ Press `Enter` 動作実行 ..."
    # raw_input()
    # tutorial.execute_plan(cartesian_plan)

    print "============ Python tutorial demo complete!"
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()