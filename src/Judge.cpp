#include <cstdio>
#include <vector>
#include <cstring>
#include <queue>
#include <cmath>
#include <algorithm>

//#define __debug__

#define Troops 3
#define Resources 4
#define Re 2

using namespace std;

pair<int, int>emy[Troops], us[Troops], sor[Resources];
int t1 = 0, t2 = 0, t3 = 0;
int dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};

/*
	如果改变来了地图的尺寸，记得更改这里的vis数组大小
*/
int xSiz, ySiz;
char vis[Troops << 1][22][22];

queue<pair<int, int> >q;

inline bool In_map(int x, int y) {
	return x >= 1 && x <= xSiz && y >= 0 && y < ySiz;
}

void bfs(int id, int x, int y, char *mps[]) {
	vis[id][x][y] = 0;
	while (!q.empty()) q.pop();
	q.push(make_pair(x, y));
	pair<int, int>now, nex;
	while (!q.empty()) {
		now = q.front(); q.pop();
		for (int i = 0; i < 4; i++) {
			int nexx = now.first + dx[i];
			int nexy = now.second + dy[i];
			if (In_map(nexx, nexy) && vis[id][nexx][nexy] == -1 && mps[nexx][nexy] != '#') {
				nex.first = nexx;
				nex.second = nexy;
				vis[id][nexx][nexy] = vis[id][now.first][now.second] + 1;
				q.push(nex);
			}
		}
	}
}

vector<int>as[Resources], ds[Resources];

inline bool Can_Win(int a, int d) {
#ifdef __debug__
	int tmpa = a, tmpd = d;
#endif
	for (int i = 0; i < Resources; i++) ds[i].clear(), as[i].clear();
	for (int i = 0; i < Troops; i++, a /= Resources, d /= Resources) {
		as[a % Resources].push_back(vis[i][sor[a % Resources].first][sor[a % Resources].second]);
		ds[d % Resources].push_back(vis[Troops + i][sor[d % Resources].first][sor[d % Resources].second]);
	}
	int cnt = 0;
	for (int i = 0; i < Resources; i++) {
		if (ds[i].size() < as[i].size()) cnt++;
		else {
			sort(as[i].begin(), as[i].end());
			sort(ds[i].begin(), ds[i].end());
			for (int j = 0; j < as[i].size(); j++) {
				if (as[i][j] < ds[i][j]) { cnt++; break; }
			}
		}
	}
#ifdef __debug__
	printf("d=%d cnt=%d ---------\n", tmpd, cnt);
	for (int i = 0; i < Resources; i++) {
		printf("i:%d A  -VS-  D\n", i);
		for (int j = 0; j < as[i].size(); j++) printf("%d ", as[i][j]); printf("  -VS-  ");
		for (int j = 0; j < ds[i].size(); j++) printf("%d ", ds[i][j]); printf("\n");
	}
#endif
	if (cnt >= Re) return false;
	else return true;
}

/*
argv[0]:-
argv[1] ~ argv[argc - 1]:maps
*/

int main(int argc, char *argv[]) {
	memset(vis, -1, sizeof(vis));
	xSiz = argc - 1;
	ySiz = strlen(argv[1]);

#ifdef __debug__
	printf("xSiz = %d , ySiz = %d\n", xSiz, ySiz);

	for (int i = 1; i <= xSiz; i++) printf("%s\n", argv[i]);
#endif

	for (int i = 1; i <= xSiz; i++) {
		for (int j = 0; j < ySiz; j++) {
			if (argv[i][j] == 'A') emy[t1++] = make_pair(i, j);
			else if (argv[i][j] == 'D') us[t2++] = make_pair(i, j);
			else if (argv[i][j] == '$') sor[t3++] = make_pair(i, j);
		}
	}
#ifdef __debug__
	printf("reading .. finish !\n");
#endif

	for (int i = 0; i < Troops; i++) bfs(i, emy[i].first, emy[i].second, argv);
	for (int i = 0; i < Troops; i++) bfs(Troops + i, us[i].first, us[i].second, argv);

#ifdef __debug__
	for (int i = 0; i < Troops << 1; i++) {
		printf("id = %d------------\n", i);
		for (int j = 1; j <= xSiz; j++) {
			for (int k = 0; k < ySiz; k++)
				printf("%d", vis[i][j][k]);
			printf("\n");
		}
	}


	Can_Win(36, 36);
	return 0;
#endif
	int all = pow(Resources, Troops) + 0.5;
#ifdef __debug__
	printf("all = %d\n", all);
#endif
	for (int s = 0; s < all; s++) {
		bool flag = false;
		for (int o = 0; o < all; o++) {
			flag = Can_Win(s, o);
			if (flag) break;
		}
		if (!flag) {
			//printf("lose!\n");		//losing
			return -1;
		}
		
	}

	//printf("win!\n");		//win

	return 1;
}