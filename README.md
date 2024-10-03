# Codeforces Assistant

**Description**

This is a simple script that can be used to get some information related to any codeforces profile. The scirpt is written in Python, and it communicates with codeforces api, and performs some operations to get the required information.

**Usage**

The script is easy to use. You just need a program that can compile and run Pyhton codes. The script also uses the time, json and requests packages so make sure to install them. It can perform 4 tasks:
  1. Creates two lists, the first one contains all problems solved during an "Out Of Competition" participation. The second list contains all problems solved during an official participation. Virtual participations are ignored, and both lists are sorted in increasing order of problem's rating. It may ignore new problems if the problem's rating hasn't been added yet.
  2. Creates a list of all problems that weren't solved during virtual participations (gyms only). Team participation is also considered since it's meant to improve team performance.
  3. Given a specific problem tag (it's also possible to consider all tags) and a difficulty range, it can find the number of solved problems with the given tag, that has a difficulty covered by the given range. It will also provide a list of these problems.
