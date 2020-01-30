#include<bits/stdc++.h>
using namespace std;

#define LL long long
#define UI unsigned int
#define MX 10000

UI seed;
double cutoff_time;
chrono::steady_clock::time_point start;

struct edgeInfo
{
    int x,y;
};
int v_num,e_num;

edgeInfo edge[MX];
LL edge_weight[MX];

vector<int>v_edges[MX],v_adj[MX];
int v_degree[MX];
LL v_weight[MX];
double avg_degree;

int c_size;
bool v_in_c[MX],save_v_in_c[MX];
LL now_weight;
int best_c_size;
bool best_v_in_c[MX];
LL best_weight;
double best_comp_time;
LL best_step;

LL dscore[MX];
LL v_age[MX];
LL v_valid_score[MX];

int remove_node_list[MX];
int index_in_remove_node_list[MX];
int remove_node_list_size;

int uncover_edge_list[MX];
int pos_in_uncover_edge_list[MX];
int uncover_edge_list_size;

int removed_list[MX];
int removed_list_size;

LL step;


double TimeElapsed();
void clear_all();
int BuildInstance(string fileName);
void UpdateBestSolution();
void SetRemoveNode();
void ConstructVC();
void Uncover(int e);
void Cover(int e);
void Add(int v);
void Remove(int v);
void RemoveRedundant();
int ChooseAddV();
int ChooseRemoveV_1();
int ChooseRemoveV_21();
int ChooseRemoveV_22();
int DynamicChoose(int &no_improve,int alpha);
void CalculateScore();
void UpdateEdgeWeight();
void LocalSearch();
void DynWVC(bool flag);
bool CheckSolution(bool flag);


double TimeElapsed()
{
    chrono::steady_clock::time_point finish = chrono::steady_clock::now();
    chrono::duration<double> duration = finish - start;
    return duration.count();
}

void clear_all()
{
    remove_node_list_size = 0;
    uncover_edge_list_size = 0;

    for(int i=0; i<=v_num; i++)
    {
        v_edges[i].clear();
        v_adj[i].clear();
    }

    fill_n(edge_weight, e_num, 1);
    fill_n(v_degree, v_num + 1, 0);
    fill_n(v_in_c, v_num + 1, false);
    fill_n(best_v_in_c, v_num + 1, false);
    fill_n(dscore, v_num + 1, 0);
    fill_n(v_age, v_num + 1, 0);
    fill_n(v_valid_score, v_num + 1, 0);
    fill_n(index_in_remove_node_list, v_num + 1, 0);
    fill_n(pos_in_uncover_edge_list, e_num, 0);
}

int BuildInstance(string fileName)
{
    ifstream infile(fileName);
    if(!infile) return  0;

    int x,y;

    infile >> v_num >> e_num;
    clear_all();
    for(int i=1; i<=v_num; i++) infile >> x >> v_weight[i];
    for(int i=0; i<e_num; i++)
    {
        infile >> x >> y;
        v_degree[x]++;
        v_degree[y]++;
        edge[i].x = x;
        edge[i].y = y;
    }
    infile.close();

    avg_degree = 0.0;
    for(int i=1; i<=v_num; i++) avg_degree += (double)v_degree[i];
    avg_degree /= (double)v_num;

    for(int i=0; i<e_num; i++)
    {
        x = edge[i].x;
        y = edge[i].y;

        v_edges[x].push_back(i);
        v_edges[y].push_back(i);

        v_adj[x].push_back(y);
        v_adj[y].push_back(x);
    }

    return  1;
}

void UpdateBestSolution()
{
    if(now_weight<best_weight && CheckSolution(false))
    {
        for(int i=1; i<=v_num; i++) best_v_in_c[i] = v_in_c[i];
        best_weight = now_weight;
        best_c_size = c_size;
        best_comp_time = TimeElapsed();
        best_step = step;
        //cout<<best_weight<<" "<<best_c_size<<endl;
    }
}

void SetRemoveNode()
{
    int j = 0;

    for(int i=1; i<=v_num; i++)
    {
        if(v_in_c[i])
        {
            remove_node_list[j] = i;
            index_in_remove_node_list[i] = j;
            j++;
        }
        else    index_in_remove_node_list[i] = 0;
    }

    remove_node_list_size = j;
}

void ConstructVC()
{
    int x,y;
    double val_x,val_y;

    c_size = 0;
    best_weight = LONG_MAX;
    now_weight = 0;

    for(int i=0; i<e_num; i++)
    {
        x = edge[i].x;
        y = edge[i].y;

        if(!v_in_c[x] && !v_in_c[y])
        {
            val_x = (double)v_degree[x]/(double)v_weight[x];
            val_y = (double)v_degree[y]/(double)v_weight[y];
            if(val_x > val_y)
            {
                v_in_c[x] = true;
                now_weight += v_weight[x];
            }
            else
            {
                v_in_c[y] = true;
                now_weight += v_weight[y];
            }
            c_size++;
        }
    }
    //cout<<best_weight<<" "<<now_weight<<endl;
    //cout<<CheckSolution(false)<<endl;
    UpdateBestSolution();

    for(int i=1; i<=v_num; i++) save_v_in_c[i] = v_in_c[i];
    int save_c_size = c_size;
    LL save_weight = now_weight;

    int times = 50;
    vector<int>blocks(e_num / 1024 + 1);
    for(int i=0; i<(e_num / 1024 + 1); i++) blocks[i] = i;

    while((times--) > 0)
    {
        fill_n(v_in_c, v_num + 1, false);
        c_size = 0;
        now_weight = 0;
        shuffle(blocks.begin(), blocks.end(), default_random_engine(seed));

        for(auto &block : blocks)
        {
            auto begin = block * 1024;
            auto end = block == e_num / 1024 ? e_num : begin + 1024;
            int tmpsize = end - begin + 1;
            vector<int>idx(tmpsize);
            for(int i=begin; i<end; i++)    idx[i - begin] = i;
            while(tmpsize > 0)
            {
                int i = rand() % tmpsize;
                edgeInfo e = edge[idx[i]];
                x = e.x;
                y = e.y;
                swap(idx[i], idx[--tmpsize]);
                if(!v_in_c[x] && !v_in_c[y])
                {
                    val_x = (double)v_degree[x]/(double)v_weight[x];
                    val_y = (double)v_degree[y]/(double)v_weight[y];
                    if(val_x > val_y)
                    {
                        v_in_c[x] = true;
                        now_weight += v_weight[x];
                    }
                    else
                    {
                        v_in_c[y] = true;
                        now_weight += v_weight[y];
                    }
                    c_size++;
                }
            }
        }
        if(now_weight < save_weight)
        {
            save_weight = now_weight;
            save_c_size = c_size;
            for(int i=1; i<=v_num; i++) save_v_in_c[i] = v_in_c[i];
        }
    }

    now_weight = save_weight;
    c_size = save_c_size;
    for(int i=1; i<=v_num; i++) v_in_c[i] = save_v_in_c[i];

    for(int i=0; i<e_num; i++)
    {
        x = edge[i].x;
        y = edge[i].y;

        if(v_in_c[x] && !v_in_c[y])         dscore[x] -= edge_weight[i];
        else if(v_in_c[y] && !v_in_c[x])    dscore[y] -= edge_weight[i];
    }

    SetRemoveNode();
    for(int i=1; i<=v_num; i++)
    {
        if(v_in_c[i] && !dscore[i]) Remove(i);
    }

    UpdateBestSolution();
}

void Uncover(int e)
{
    uncover_edge_list[uncover_edge_list_size] = e;
    pos_in_uncover_edge_list[e] = uncover_edge_list_size;
    uncover_edge_list_size++;
}

void Cover(int e)
{
    int pos = pos_in_uncover_edge_list[e];
    pos_in_uncover_edge_list[e] = 0;
    e = uncover_edge_list[--uncover_edge_list_size];
    uncover_edge_list[pos] = e;
    pos_in_uncover_edge_list[e] = pos;
}

void Add(int v)
{
    int e,x;

    v_in_c[v] = true;
    c_size++;
    dscore[v] = -dscore[v];
    now_weight += v_weight[v];
    v_valid_score[v] = 0;

    remove_node_list[remove_node_list_size] = v;
    index_in_remove_node_list[v] = remove_node_list_size++;

    for(int i=0; i<v_degree[v]; i++)
    {
        e = v_edges[v][i];
        x = v_adj[v][i];

        if(!v_in_c[x])
        {
            dscore[x] -= edge_weight[e];
            Cover(e);
            v_valid_score[v] += (v_weight[x] - v_weight[v]);
        }
        else    dscore[x] += edge_weight[e];
    }
}

void Remove(int v)
{
    int e,x;

    v_in_c[v] = false;
    c_size--;
    dscore[v] = -dscore[v];
    now_weight -= v_weight[v];
    v_valid_score[v] = 0;

    x = remove_node_list[--remove_node_list_size];
    int index = index_in_remove_node_list[v];
    index_in_remove_node_list[v] = 0;
    remove_node_list[index] = x;
    index_in_remove_node_list[x] = index;

    int limit = v_degree[v];
    for(int i=0; i<limit; i++)
    {
        e = v_edges[v][i];
        x = v_adj[v][i];

        if(!v_in_c[x])
        {
            dscore[x] += edge_weight[e];
            Uncover(e);
        }
        else    dscore[x] -= edge_weight[e];
    }
}

void RemoveRedundant()
{
    int v;
    for(int i=0; i<remove_node_list_size; i++)
    {
        v = remove_node_list[i];
        if(v_in_c[v] && !dscore[v])
        {
            Remove(v);
            i--;
        }
    }
}

int ChooseAddV()
{
    int v,limit;
    int best_v;
    LL old;
    double gain_v,max_gain = DBL_MIN;

    for(int i=0; i<removed_list_size; i++)
    {
        limit = v_degree[removed_list[i]];
        for(int j=0; j<limit; j++)
        {
            v = v_adj[removed_list[i]][j];
            if(v_in_c[v])   continue;

            gain_v = (double)abs(dscore[v])/(double)v_weight[v];
            if(gain_v > max_gain)
            {
                best_v = v;
                old = v_age[v];
                max_gain = gain_v;
            }
            else if(gain_v==max_gain && v_age[v]<old)
            {
                best_v = v;
                old = v_age[v];
            }
            if(TimeElapsed() > cutoff_time) return  0;
        }

        v = removed_list[i];
        if(v_in_c[v])   continue;

        gain_v = (double)abs(dscore[v])/(double)v_weight[v];
        if(gain_v > max_gain)
        {
            best_v = v;
            old = v_age[v];
            max_gain = gain_v;
        }
        else if(gain_v==max_gain && v_age[v]<old)
        {
            best_v = v;
            old = v_age[v];
        }
        if(TimeElapsed() > cutoff_time) return  0;
    }

    return  best_v;
}

int ChooseRemoveV_1()
{
    int v,remove_v;
    LL old;
    double loss_v,min_loss = DBL_MAX;

    for(int i=0; i<remove_node_list_size; i++)
    {
        v = remove_node_list[i];
        loss_v = (double)abs(dscore[v])/(double)v_weight[v];

        if(loss_v < min_loss)
        {
            remove_v = v;
            old = v_age[v];
            min_loss = loss_v;
        }
        else if(loss_v==min_loss && v_age[v]<v_age[remove_v])
        {
            remove_v = v;
            old = v_age[v];
        }
    }
    return  remove_v;
}

int ChooseRemoveV_21()
{
    int v,remove_v;
    LL old;
    LL score_v,min_score = LONG_MAX;

    for(int i=0; i<remove_node_list_size; i++)
    {
        v = remove_node_list[i];
        score_v = v_valid_score[v];

        if(score_v < min_score)
        {
            remove_v = v;
            old = v_age[v];
            min_score = score_v;
        }
        else if(score_v==min_score && v_age[v]<v_age[remove_v])
        {
            remove_v = v;
            old = v_age[v];
        }
    }
    return  remove_v;
}

int ChooseRemoveV_22()
{
    int v;
    LL old;
    double loss_v,min_loss;
    int remove_v = remove_node_list[rand() % remove_node_list_size];
    min_loss = (double)abs(dscore[remove_v])/(double)v_weight[remove_v];
    old = v_age[remove_v];
    int to_try = 50;

    for(int i=1; i<to_try; i++)
    {
        v = remove_node_list[rand() % remove_node_list_size];
        loss_v = (double)abs(dscore[v])/(double)v_weight[v];

        if(loss_v < min_loss)
        {
            remove_v = v;
            old = v_age[v];
            min_loss = loss_v;
        }
        else if(loss_v==min_loss && v_age[v]<v_age[remove_v])
        {
            remove_v = v;
            old = v_age[v];
        }
    }
    return  remove_v;
}

int DynamicChoose(int &no_improve, int alpha)
{
    if(no_improve<alpha)    return  ChooseRemoveV_21();
    else
    {
        no_improve = 0;
        return  ChooseRemoveV_22();
    }
}

void CalculateScore()
{
    int x,y;
    fill_n(dscore, v_num+1, 0);
    for(int i=0; i<e_num; i++)  edge_weight[i] = 1;
    for(int i=0; i<e_num; i++)
    {
        x = edge[i].x;
        y = edge[i].y;

        if(v_in_c[x] && !v_in_c[y])         dscore[x] -= edge_weight[i];
        else if(v_in_c[y] && !v_in_c[x])    dscore[y] -= edge_weight[i];
    }

    for(int i=1; i<=v_num; i++)
    {
        if(v_in_c[i])
        {
            for(int j=0; j<v_degree[i]; j++)
            {
                x = v_adj[i][j];
                if(!v_in_c[x])  v_valid_score[i] += (v_weight[x] - v_weight[i]);
            }
        }
    }
}

void UpdateEdgeWeight()
{
    int e;
    for(int i=0; i<uncover_edge_list_size; i++)
    {
        e = uncover_edge_list[i];
        edge_weight[e]++;
    }
}

void DynWVC(bool flag) /// set, flag = false for DynWVC1 and flag = true for DynWVC2
{
    ConstructVC();
    LL prev_weight = best_weight;

    CalculateScore();

    step = 1;
    int no_improve = 0,alpha = 5,v;
    double sum_degree,threshold = 2.0 * avg_degree;
    while(TimeElapsed() < cutoff_time)
    {
        sum_degree = 0.0;
        removed_list_size = 0;
        v = ChooseRemoveV_1();
        removed_list[removed_list_size++] = v;
        sum_degree += (double)v_degree[v];
        //cout<<"step -> "<<step<<", first -> "<<v<<endl;
        Remove(v);
        v_age[v] = step;

        v = DynamicChoose(no_improve, alpha);
        removed_list[removed_list_size++] = v;
        sum_degree += (double)v_degree[v];
        //cout<<"step -> "<<step<<", second -> "<<v<<endl;
        Remove(v);
        v_age[v] = step;

        if(flag && sum_degree<threshold)
        {
            v = ChooseRemoveV_22();
            removed_list[removed_list_size++] = v;
            //cout<<"step -> "<<step<<", third -> "<<v<<endl;
            Remove(v);
            v_age[v] = step;
        }

        while(uncover_edge_list_size>0 && TimeElapsed()<cutoff_time)
        {
            v = ChooseAddV();
            if(v<1 || v>v_num)  break;
            //cout<<"ChooseAddV -> "<<v<<endl;
            Add(v);
            v_age[v] = step;
            //cout<<"OK1"<<endl;
            UpdateEdgeWeight();
            //cout<<"OK2"<<endl;
            RemoveRedundant();
            //cout<<"OK3"<<endl;
        }

        UpdateBestSolution();
        if(prev_weight <= now_weight)   no_improve++;
        prev_weight = now_weight;

        step++;
        //cout<<step<<endl;
    }
}

bool CheckSolution(bool flag)
{
    if(flag)
    {
        for(int i=0; i<e_num; i++)
        {
            if(!best_v_in_c[edge[i].x] && !best_v_in_c[edge[i].y])
            {
                cout<<"uncovered edge "<<i<<endl;
                return  false;
            }
        }

        LL sum = 0;
        for(int i=1; i<=v_num; i++)
        {
            if(best_v_in_c[i])  sum += v_weight[i];
        }
        if(sum!=best_weight)    return  false;
    }
    else
    {
        for(int i=0; i<e_num; i++)
        {
            if(!v_in_c[edge[i].x] && !v_in_c[edge[i].y])
            {
                //cout<<"uncovered edge "<<i<<endl;
                return  false;
            }
        }

        LL sum = 0;
        for(int i=1; i<=v_num; i++)
        {
            if(v_in_c[i])   sum += v_weight[i];
        }
        if(sum!=now_weight) return  false;
    }
    return  true;
}
