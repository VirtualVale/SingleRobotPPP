import rosbag
from nav_msgs.msg import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

verts = [
   (1., 1.),  # left, bottom
   (1., 3.),  # left, top
   (3., 3.),  # right, top
   (3., 1.),  # right, bottom
   (0., 0.),  # ignored
]

codes = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY,
]

path = Path(verts, codes)

bag = rosbag.Bag('./2020-10-05-21-59-50.bag')
topic = '/move_base/NavfnROS/plan'
column_names = ['start_time', 'x', 'y']
data = []
#df = pd.DataFrame(columns = column_names)
path_id = -1

for topic, msg, t in bag.read_messages(topics=topic):
	
	path_id = path_id + 1
	start_time = msg.header.stamp

	for i in range(len(msg.poses)):
		x_pos = msg.poses[i].pose.position.x
		y_pos = msg.poses[i].pose.position.y
		#print(start_time)
		#df.append({'start_time': start_time, 'x': start_time, 'y': start_time}, ignore_index=True)
		data.append([path_id, start_time, x_pos , y_pos])

print(len(data))
df = pd.DataFrame(data, columns = ['path_id','startTime', 'x', 'y'])
print(df.head())
ax = df.plot(kind="scatter", x="x", y="y", alpha=0.1)
patch = patches.PathPatch(path, facecolor='orange', lw=2)
ax.add_patch(patch)
plt.show()
df.to_csv('script.csv')
