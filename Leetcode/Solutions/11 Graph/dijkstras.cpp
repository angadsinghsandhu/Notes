#include <iostream>
#include <vector>
#include <limits.h>

using namespace std;

#define V 9

void show(vector<int> dist){
    for(int v=0; v<V; v++){
        cout << "( " << v << " : " << dist[v] << " )\n";
    }
}

void showBool(vector<bool> visited){
    for(int v=0; v<V; v++){
        if(visited[v])
            cout << "true ";
        else
            cout << "false ";
    }
    cout << endl;
}


int getMin(vector<int> dist, vector<bool> visited){
    int min = INT_MAX, vertex_min;
    
    for(int v=0; v<V; v++){
        if(!visited[v] && dist[v] <= min){
            min = dist[v];
            vertex_min = v;
        }
    }
    
    return vertex_min;
}


void dijkstra(int graph[V][V], int start){
    // creating dist array to store minimum distamces
    vector<int> dist(V, INT_MAX);
    
    // create visited array to store if a specific arry has been traversed previously
    vector<bool> visited(V,false);
    
    // setting the first point as 0 and true
    dist[start] = 0;
    
    int u;
    // finding minimum distance
    for(int count=0; count<V-1; count++){
        u = getMin(dist, visited);
        visited[u] = true;
        
        for(int v=0; v<V; v++){
            if(graph[u][v]!=0 && dist[u]!=INT_MAX && !visited[v] 
                && dist[u]+graph[u][v]<dist[v])
                    dist[v] = dist[u] + graph[u][v];
        }
    }
    show(dist);
}


// driver program to test above function
int main()
{
   
    /* Let us create the example graph discussed above */
    int graph[V][V] = { { 0, 4, 0, 0, 0, 0, 0, 8, 0 },
                        { 4, 0, 8, 0, 0, 0, 0, 11, 0 },
                        { 0, 8, 0, 7, 0, 4, 0, 0, 2 },
                        { 0, 0, 7, 0, 9, 14, 0, 0, 0 },
                        { 0, 0, 0, 9, 0, 10, 0, 0, 0 },
                        { 0, 0, 4, 14, 10, 0, 2, 0, 0 },
                        { 0, 0, 0, 0, 0, 2, 0, 1, 6 },
                        { 8, 11, 0, 0, 0, 0, 1, 0, 7 },
                        { 0, 0, 2, 0, 0, 0, 6, 7, 0 } };
 
    dijkstra(graph, 0);
 
    return 0;
}