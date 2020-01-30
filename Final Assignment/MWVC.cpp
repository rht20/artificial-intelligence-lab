#include<bits/stdc++.h>
#include "MWVC.h"
using namespace std;

int main(int argc, char *argv[])
{
    if(argc != 3)
    {
        cerr << "Follow this format: ./mwvc [Graph file] [Cutoff time]" << endl;
        return  0;
    }

    stringstream ss;
    ss << argv[2];
    ss >> cutoff_time;
    ss.clear();
    if(cutoff_time < 0 || cutoff_time > (int)(~0U>>1))  cutoff_time = 60.0;

    srand(time(NULL));

    if(!BuildInstance(argv[1]))
    {
        cerr << "Open instance file failed." << endl;
        return  0;
    }

    cout << "Input File: " << argv[1] << endl;

    cout<<"DynWVC1:"<<endl;
    start = chrono::steady_clock::now();
    DynWVC(false);
    if(CheckSolution(true) == 1)
    {
        cout << "best_weight = " << best_weight << endl;
        //cout << "best_c_size = " << best_c_size << endl;
        //cout << "best_comp_time = " << best_comp_time << endl;
    }
    else    cout << "The solution is wrong." << endl;

    if(!BuildInstance(argv[1]))
    {
        cerr << "Open instance file failed." << endl;
        return  0;
    }
    cout<<"DynWVC2:"<<endl;
    start = chrono::steady_clock::now();
    DynWVC(true);
    if(CheckSolution(true) == 1)
    {
        cout << "best_weight = " << best_weight << endl;
        //cout << "best_c_size = " << best_c_size << endl;
        //cout << "best_comp_time = " << best_comp_time << endl;
    }
    else    cout << "The solution is wrong." << endl;

    //cout << TimeElapsed() << endl;

    return  0;
}
