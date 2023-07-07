

#include <iostream>
#include <vector>
#include <list>
#include <stack>

using namespace std;


class Graph{
    // number of vertices
    int V;
    
    // creating a vector to keep track if we have visited a nodes
    vector<bool> visited;
    
    // adjacency list
    vector<vector<int>> adj;
    
public:
    Graph(int V); // constructor
    
    void showAdj();
    
    void addEdge(int v, int m);
    
    void BFS(int s);
    
    void DFS(int s);
};

Graph::Graph(int V){
    this->V = V;
    adj = vector<vector<int>>(V);
    visited = vector<bool>(V, false);
}

void Graph::showAdj(){
    for(int i=0; i<adj.size(); i++){
        cout << "Vertices connected to " << i << ": ";
        for(auto j: adj[i])
            cout << j << " ";
        cout << endl;
    }
}

void showLst(list<int> arr){
    for(auto j: arr)
        cout << j << " ";
    cout << endl;
}

void Graph::addEdge(int v, int m){
    adj[v].push_back(m);
}

void Graph::BFS(int s){
    // create queue to keep track of unvisited nodes
    list<int> queue;
    
    // visiting our starting node
    visited[s] = true;
    queue.push_back(s);
    
    // creating iterator
    vector<int>::iterator it;
    
    // traversing over all nodes
    while(!queue.empty()){
        s = queue.front();
        cout << s << " ";
        queue.pop_front();
        
        for(it=adj[s].begin(); it!=adj[s].end(); it++){
            if(!visited[*it]){
                visited[*it] = true;
                queue.push_back(*it);
            }
        }
    }
    cout << endl;
}

void Graph::DFS(int s){
    // set current node as visited and print
    visited[s]= true;
    cout << s << " ";
    
    // creating iterartor
    vector<int>::iterator it; 
    
    // recur to all nodes
    for(it=adj[s].begin(); it!=adj[s].end(); it++){
        if(!visited[*it])
            DFS(*it);
    }
    
}

int main()
{
    Graph g(4);
    
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    
    g.addEdge(1, 2);
    
    g.addEdge(2, 0);
    g.addEdge(2, 3);
    
    g.addEdge(3, 3);
    
    // g.showAdj();
    
    // g.BFS(2);
    g.DFS(2);

    return 0;
}
