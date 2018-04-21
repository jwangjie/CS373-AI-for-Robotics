/* Shortest Time Challenge

Author: Jie Wang
Time:   May 16, 2017

*/

#include<iostream>
#include<cmath>
#include<iomanip>
using std::sqrt;
using std::cin;
using std::cout;
using std::setprecision;
using std::fixed;
#define INF 1e7

//define waypoints data structure
struct waypoints{
	int x;	  // x
	int y;	  // y
	double p; // skip penalty
};

// distance calcualation
double dist(waypoints a,waypoints b){
	return sqrt(double((a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y)));
}

waypoints point[1002]; // starting point 0, N waypoints, goal point N+1
double Time[1002];     // time cost of waypoint k
int N;             // 1 to 1000 waypoints

void dijkstra(){
	for(int i = 0; i < N+2; i++){		 // for every start vertex

		double sum = 0;
		for(int j = i+1; j < N+2; j++){	 // for every end vertex 

			if(j > i+1){                // if skip waypoint, add penalty
				sum += point[j-1].p;   // sum of the time penalty
			}

			if(Time[j] > Time[i] + dist(point[i], point[j]) / 2 + sum + 10){	// update the minimum time if possible 
				Time[j] = Time[i] + dist(point[i], point[j]) / 2 + sum + 10;
			}
		}
	}
	cout << fixed << setprecision(3) << Time[N+1] << "\n";
}

int main(){

	while(1){
		cin >> N;  // input waypoints number

		if(N == 0){
			break;
		}

		bool error = false; // inputs boundary flag
		for(int i = 1; i < N+1; i++){
			cin >> point[i].x >> point[i].y >> point[i].p;

			if(point[i].x < 1 || point[i].x > 99 || point[i].y < 1 || point[i].y >99 || point[i].p < 1 || point[i].p >100){
				error = true;
			}	

			Time[i] = INF;  // // initialize time cost of all waypoints as infinite, time cost to starting point as 0
			Time[0] = 0;   // starting point time = 0
			Time[N+1] = INF;   

			if(error){
				cout << "Out of the inputs boundary\n"; // the waypoints position or the skip time penalty inputs error
				cin >> N;
				continue;
			}
		}

		point[0].x = 0; 
		point[0].y = 0; 
		point[0].p = 0;	      // set starting point

		point[N+1].x = 100;
		point[N+1].y = 100;   // set goal point

		dijkstra();
	}
}



/*
// Question //

A course is set up in a 100m by 100m factory. Certain points are identified within the space as waypoints to 
visit to receive goods. They are ordered -- there is a waypoint 1, a waypoint 2, etc. Your robot must start 
at (0,0). From there, it should go to waypoint 1, stop for 10 second, go to waypoint 2, stop for 10 second, 
and so on. It must finally end up at, and stop for 10 second on (100,100).

Each waypoint except (0,0) and (100,100) has a time penalty for missing the load to reflect the time needed for a 
human to handle the work later. So, if your robot went straight from waypoint 1 to waypoint 3, skipping waypoint 2, 
it would incur waypoint 2's penalty. Note that once it hits waypoint 3, it cannot go back to waypoint 2. It must 
hit the waypoint in order. Since your robot must stop for 10 seconds on each waypoint to be loaded, it is not in 
danger of hitting a waypoint accidentally too soon. For example, if waypoint 3 lies directly between waypoints 1 
and 2, your robot can go straight from 1 to 2, right over 3, without stopping. Since it didn't stop to be loaded, 
waypoint 3's penalty will not be incurred. Your final score is the amount of time (in seconds) your robot takes to 
reach (100,100), completing the course, plus all penalties. Smaller scores are better.

Assume your robot is very maneuverable, but a bit slow. It moves at 2 m/s, but can turn very quickly. During the 
10 seconds, it stops on a waypoint point, it can easily turn to face the next waypoint. Thus, it can always move 
in a straight line between target points.

Because your robot is a bit slow, it might be advantageous to skip some waypoints and incur their penalty, rather than 
actually maneuvering to them. Given a description of a course, determine your robot's best (lowest) possible time.

// Input //

There will be several test cases fed into your solution via stdin. Each test case will begin with a line with one 
integer, N (1 <= N <= 1000) which is the number of waypoints on the course. Each of the next N lines will describe 
a waypoint with three integers, X, Y and P, where (X, Y) is a location on the course ( 1 <= X, Y <= 99, X and Y in 
meters) and P is the penalty incurred if OTTO misses that waypoint (1 <= P <= 100). The waypoints will be given in 
order -- the first line after N is target 1, the next is waypoint 2, and so on. All the waypoints on a given course 
will be unique -- there will be at most one waypoint point at any location on the course. End of input will be 
marked by a line with a single '0'.

// Output //

For each test case, output a single decimal number, indicating the smallest possible time for that course. Output 
this number rounded (NOT truncated) to three decimal places. Print each answer on its own line on stdout and do not 
print any blank lines between answers.

// Sample Input //
1
50 50 20
3
30 30 90
60 60 80
10 90 100
3
30 30 90
60 60 80
10 90 10
0

// Sample Output //
90.711
156.858
110.711
*/
