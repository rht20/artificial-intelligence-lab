#include<bits/stdc++.h>
using namespace std;

#define MX  10
#define PII pair<int,int>
struct data
{
    int score,row,col;
};
int n;
char board[MX][MX];

void printBoard()
{
    for(int i=0; i<n; i++)
    {
        for(int j=0; j<n; j++)  cout<<board[i][j];
        cout<<endl;
    }
    return;
}

bool moveLeft()
{
    for(int i=0; i<n; i++)
    {
        for(int j=0; j<n; j++)
        {
            if(board[i][j]=='-')    return  true;
        }
    }
    return  false;
}

bool check()
{
    /// check row
    for(int i=0; i<n; i++)
    {
        bool flag = true;
        for(int j=1; j<n; j++)
        {
            if(board[i][j-1]!=board[i][j])
            {
                flag = false;
                break;
            }
        }
        if(flag)
        {
            if(board[i][0]=='X')
            {
                puts("Winner: Human");
                return  true;
            }
            else if(board[i][0]=='O')
            {
                puts("Winner: Computer");
                return  true;
            }
        }
    }

    /// check column
    for(int j=0; j<n; j++)
    {
        bool flag = true;
        for(int i=1; i<n; i++)
        {
            if(board[i-1][j]!=board[i][j])
            {
                flag = false;
                break;
            }
        }
        if(flag)
        {
            if(board[0][j]=='X')
            {
                puts("Winner: Human");
                return  true;
            }
            else if(board[0][j]=='O')
            {
                puts("Winner: Computer");
                return  true;
            }
        }
    }

    /// check left diagonal
    bool flag = true;
    for(int i=1; i<n; i++)
    {
        for(int j=i; j<=i; j++)
        {
            if(board[i-1][j-1]!=board[i][j])    flag = false;
        }
        if(!flag)   break;
    }
    if(flag)
    {
        if(board[0][0]=='X')
        {
            puts("Winner: Human");
            return  true;
        }
        else if(board[0][0]=='O')
        {
            puts("Winner: Computer");
            return  true;
        }
    }

    /// check right diagonal
    flag = true;
    for(int i=1; i<n; i++)
    {
        for(int j=n-i-1; j<=n-i-1; j++)
        {
            if(board[i-1][n-i]!=board[i][j])    flag = false;
        }
        if(!flag)   break;
    }
    if(flag)
    {
        if(board[0][n-1]=='X')
        {
            puts("Winner: Human");
            return  true;
        }
        else if(board[0][n-1]=='O')
        {
            puts("Winner: Computer");
            return  true;
        }
    }

    if(!moveLeft())
    {
        cout << "Match draw" << endl;
        return  true;
    }

    return  false;
}

int getScore()
{
    /// check row
    for(int i=0; i<n; i++)
    {
        bool flag = true;
        for(int j=1; j<n; j++)
        {
            if(board[i][j-1]!=board[i][j])
            {
                flag = false;
                break;
            }
        }
        if(flag)
        {
            if(board[i][0]=='X')    return  1;
            else if(board[i][0]=='O')   return  -1;
        }
    }

    /// check column
    for(int j=0; j<n; j++)
    {
        bool flag = true;
        for(int i=1; i<n; i++)
        {
            if(board[i-1][j]!=board[i][j])
            {
                flag = false;
                break;
            }
        }
        if(flag)
        {
            if(board[0][j]=='X')    return  1;
            else if(board[0][j]=='O')   return  -1;
        }
    }

    /// check left diagonal
    bool flag = true;
    for(int i=1; i<n; i++)
    {
        for(int j=i; j<=i; j++)
        {
            if(board[i-1][j-1]!=board[i][j])    flag = false;
        }
        if(!flag)   break;
    }
    if(flag)
    {
        if(board[0][0]=='X')    return  1;
        else if(board[0][0]=='O')   return  -1;
    }

    /// check right diagonal
    flag = true;
    for(int i=1; i<n; i++)
    {
        for(int j=n-i-1; j<=n-i-1; j++)
        {
            if(board[i-1][n-i]!=board[i][j])    flag = false;
        }
        if(!flag)   break;
    }
    if(flag)
    {
        if(board[0][n-1]=='X')  return  1;
        else if(board[0][n-1]=='O')   return  -1;
    }

    return  0;
}

int MinMax(bool isMax)
{
    int score = getScore();
    if(score)   return  score;

    if(!moveLeft()) return  0;

    int best;
    if(isMax)
    {
        best = -10;
        for(int i=0; i<n; i++)
        {
            for(int j=0; j<n; j++)
            {
                if(board[i][j]=='-')
                {
                    board[i][j] = 'X';
                    best = max(best, MinMax(!isMax));
                    board[i][j] = '-';
                }
            }
        }
    }
    else
    {
        best = 10;
        for(int i=0; i<n; i++)
        {
            for(int j=0; j<n; j++)
            {
                if(board[i][j]=='-')
                {
                    board[i][j] = 'O';
                    best = min(best, MinMax(!isMax));
                    //cout<<best<<" "<<i<<" "<<j<<endl;
                    board[i][j] = '-';
                }
            }
        }
    }
    return  best;
}

void getMove()
{
    data bestMove = {10, -1, -1};
    for(int i=0; i<n; i++)
    {
        for(int j=0; j<n; j++)
        {
            if(board[i][j]=='-')
            {
                board[i][j] = 'O';
                int score = MinMax(true);
                //cout<<i<<" "<<j<<" "<<score<<endl;
                if(score < bestMove.score)  bestMove = {score, i, j};
                board[i][j] = '-';
            }
        }
    }
    board[bestMove.row][bestMove.col] = 'O';
    cout << "Computer Move:\nOptimal value = " << bestMove.score << ", Row = " << bestMove.row << ", Column = " << bestMove.col << endl;
    return;
}

void playGame(bool player)
{
    PII pos;
    while(!check())
    {
        if(player)
        {
            cout << "Your move:";
            cin >> pos.first >> pos.second;
            board[pos.first][pos.second] = 'X';
        }
        else    getMove();

        printBoard();
        player ^= true;
    }
    return;
}

int main()
{
    int player;
    while(1)
    {
        cout << "Board size: ";
        cin >> n;
        cout << "First Move:\n1. Player\n2. Computer" << endl;
        cin >> player;

        memset(board,'-',sizeof(board));
        printBoard();
        if(player==1)   playGame(true);
        else            playGame(false);
    }
    return  0;
}
