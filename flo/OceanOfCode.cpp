#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
namespace
{
    constexpr int kWidth = 15;
    constexpr int kHeight = 15;
}

/*
/* ####################################
/* Submarine
/* ####################################
*/

class Submarine
{
private:    
    int m_x;
    int m_y;
    
    bool m_isKnownPosition;
	
	int m_torpedoCooldown;

public:
    Submarine() :
    m_isKnownPosition(false)
    {
    };
    
    Submarine(const int x, const int y, const int torpedoCooldown) : 
    m_x(x),
    m_y(y),
    m_isKnownPosition(true),
	m_torpedoCooldown(torpedoCooldown)
    {};
    
    int getX() const { return m_x; }
    int getY() const { return m_y; }
	
	bool canShootTorpedo() const { return m_torpedoCooldown == 0; }
    
    void print() const
    {
        if (m_isKnownPosition)
            cerr << "x = " << m_x << "; y = " << m_y << endl;
        else
            cerr << "Unkown position" << endl;
		cerr << "torpedo cooldown: " << m_torpedoCooldown << endl;
    }
};

/*
/* ####################################
/* Point
/* ####################################
*/

struct Point
{
    int x;
    int y;
    
    Point() {};
    Point(const int x_, const int y_) : x(x_), y(y_) {};
    
};

bool operator==(Point const& p1, Point const& p2) { return (p1.x == p2.x && p1.y == p2.y); } 

/*
/* ####################################
/* Direction
/* ####################################
*/

enum Direction
{
    kNorth,
    kEast,
    kSouth,
    kWest
};

#define Delta Point

Delta direction2delta(const Direction direction)
{
   switch (direction)
   {
       case Direction::kNorth:
       return Delta(0, -1);
       case Direction::kEast:
       return Delta(1, 0);
       case Direction::kSouth:
       return Delta(0, 1);
       case Direction::kWest:
       return Delta(-1, 0);
   }
}

Direction delta2direction(const Delta delta)
{
    if (delta == Delta(0, -1))
        return Direction::kNorth;
    else if (delta == Delta(0, 1))
        return Direction::kSouth;
    else if (delta == Delta(-1, 0))
        return Direction::kWest;
    else
        return Direction::kEast;
}

/*
/* ####################################
/* Map
/* ####################################
*/

class Map
{
protected:
std::array<std::array<int, kHeight>, kWidth> m_cells;
   
bool set(const int x, const int y, const int value)
{
   if (x < 0 || x >= kWidth || y < 0 || y >= kHeight)
   {
       cerr << "Coordinates out of map" << endl;
       return false;
   }
   
   m_cells[x][y] = value;
}
    
public:
    Map(const int defaultValue)
    {
        for (int x = 0; x < kWidth; x++)
        {
            for (int y = 0; y < kHeight; y++)
            {
                m_cells[x][y] = 0;
            }
        }
    }
    
    void print() const
    {
        for (int y = 0; y < kHeight; y++)
        {
            for (int x = 0; x < kWidth; x++)
            {
                cerr << m_cells[x][y];
            }
            cerr << endl;
        }
    }
            
};

/*
/* ####################################
/* MoveMap
/* ####################################
*/

class MoveMap : public Map
{
private:
    
    enum CellType
    {
        kEmpty,
        kIsland,
        kPath
    };
    
public:
    MoveMap() : Map(CellType::kEmpty) {};
    
    bool setIsland(const int x, const int y)
    {
        this->set(x, y, CellType::kIsland);
    }
    
    bool setPath(const int x, const int y)
    {
        this->set(x, y, CellType::kPath);
    }
    
    bool isMovable(const int x, const int y) const
    {
        if (x < 0 || x >= kWidth || y < 0 || y >= kHeight)
        {
            return false;
        }
        
        return m_cells[x][y] == CellType::kEmpty;
    }
    
    void reset()
    {
        for (int y = 0; y < kHeight; y++)
        {
            for (int x = 0; x < kWidth; x++)
            {
                if (m_cells[x][y] == CellType::kPath)
                    m_cells[x][y] = CellType::kEmpty;
            }
        }
    }
    
    void getInitialPosition()
    {
        for (int y = 0; y < kHeight; y++)
        {
            for (int x = 0; x < kWidth; x++)
            {
                if (m_cells[x][y] == CellType::kEmpty)
                {
                    cout << x << " " << y << endl;
                    return;
                }
            }
        }
    }
};

/*
/* ####################################
/* OppOriginMap
/* ####################################
*/

class OppOriginMap : public Map
{
private:
  enum CellType
  {
      kYes,
      kNo,
      kTmp
  };
public:
    OppOriginMap(const MoveMap& moveMap) : Map(kYes)
    {
        for (int y = 0; y < kHeight; y++)
        {
            for (int x = 0; x < kWidth; x++)
            {
                if (!moveMap.isMovable(x, y))
                {
                    m_cells[x][y] = CellType::kNo;
                }
            }
        }
    }
    
    void update(const int dx, const int dy)
    {
        for (int y = 0; y < kHeight; y++)
        {
            for (int x = 0; x < kWidth; x++)
            {
                if (x + dx >= 0 && x + dx < kWidth && y + dy >= 0 && y + dy < kHeight)
                {
                    if (m_cells[x + dx][y + dy] == CellType::kNo)
                    {
                        m_cells[x][y] = CellType::kTmp;
                    }
                }
                else
                {
                    m_cells[x][y] = CellType::kTmp;
                }
            }
        }
    }
	
	bool isOriginCandidate(const int x, const int y) const
	{
		if (x < 0 || x >= kWidth || y < 0 || y >= kHeight)
			return false;
		
		return m_cells[x][y] == CellType::kYes;
	}
    
};

/*
/* ####################################
/* OppPoisitionMap
/* ####################################
*/

class OppPositionMap : public Map
{
private:

public:
    OppPositionMap(const OppOriginMap& oppOriginMap, const int dx, const int dy) : Map(0)
    {
        for (int y = 0; y < kHeight; y++)
        {
            for (int x = 0; x < kWidth; x++)
            {
                if (oppOriginMap.isOriginCandidate(x - dx, y - dy))
                {
                    m_cells[x][y] = 1;
                }
				else
				{
					m_cells[x][y] = 0;
				}
            }
        }
    }

	bool canBeOpp(const int x, const int y) const
	{
		if (x < 0 || x >= kWidth || y < 0 || y >= kHeight)
			return false;
		
		return m_cells[x][y] == 1;
	}
	
	Point getBarycenter()
	{
	    int s_x = 0;
	    int s_y = 0;
	    int n = 0;
	    for (int x = 0; x < kWidth; x++)
        {
            for (int y = 0; y < kHeight; y++)
            {
                const int value = m_cells[x][y];
                s_x += value * x;
                s_y += value * y;
                n += value;
            }
        }
        
        Point barycenter;
        barycenter.x = s_x / n;
        barycenter.y = s_y / n;
        
        return barycenter;
	}
};

/*
/* ####################################
/* Player
/* ####################################
*/

class Player
{
private:
    const int m_id;
    Submarine m_submarine;
    int m_life;
public:
    Player (const int id) :
    m_id(id)
    {       
    };
    
    Submarine getSubmarine() const { return m_submarine; }
    
    void setSubmarine(const int x, const int y, const int torpedoCooldown)
    {
        m_submarine = Submarine(x, y, torpedoCooldown);
    }
    
    void setLife (const int life)
    {
        m_life = life;
    }
    
    void print() const
    {
        cerr << "Player id: " << m_id << endl;
        cerr << "Player life: " << m_life << endl;
        cerr << "Submarine:" << endl;
        m_submarine.print();
    }
};


/*
/* ####################################
/* OppFinder
/* ####################################
*/

class OppFinder
{
private:
	OppOriginMap m_oppOriginMap;
	OppPositionMap m_oppPositionMap;
	
	int m_dx;
	int m_dy;
	
public:
	OppFinder(const MoveMap& moveMap) :
	m_dx(0),
	m_dy(0),
	m_oppOriginMap(moveMap),
	m_oppPositionMap(m_oppOriginMap, m_dx, m_dy)
	{
        m_oppPositionMap = OppPositionMap(m_oppOriginMap, m_dx, m_dy);
	}
	
	void update(const int dx, const int dy)
	{
		m_dx += dx;
		m_dy += dy;
		
		m_oppOriginMap.update(m_dx, m_dy);
		m_oppPositionMap = OppPositionMap(m_oppOriginMap, m_dx, m_dy);
	}
	
	bool canBeOpp(const int x, const int y) const
	{
		return m_oppPositionMap.canBeOpp(x, y);
	}
	
	Point getBarycenter()
	{
	    return m_oppPositionMap.getBarycenter();
	}
	
	void print() const
	{
	    cerr << "oppOriginMap" << endl;
	    m_oppOriginMap.print();
	    cerr << "oppPositionMap" << endl;
		m_oppPositionMap.print();
	}
	
};

/*
/* ####################################
/* Game
/* ####################################
*/

class Game
{
private:
    Player m_myPlayer;
    Player m_oppPlayer;
    MoveMap* m_moveMap;
	OppFinder m_oppFinder;
    
    void move(const Direction direction)
    {
        switch (direction)
        {
            case kNorth:
                cout << "MOVE N";
                break;
            case kEast:
                cout << "MOVE E";
                break;
            case kSouth:
                cout << "MOVE S";
                break;
            case kWest:
                cout << "MOVE W";
                break;
        }
    }
	
	void shootTorpedo(const int x, const int y)
	{
		cout << "TORPEDO " << x << " " << y;
	}
    
    void surface() 
    { 
        cout << "SURFACE";
        m_moveMap->reset();
    }
    
    void chargeTorpedo() { cout << " TORPEDO"; }
    
    void newAction() { cout << "|"; }
    
    void endAction() { cout << endl; }
    
    
public:
    Game(const Player& myPlayer, const Player& oppPlayer, MoveMap* moveMap, const OppFinder& oppFinder) :
    m_myPlayer(myPlayer),
    m_oppPlayer(oppPlayer),
    m_moveMap(moveMap),
	m_oppFinder(oppFinder)
    {  
    };
	
	bool findAndAttack()
	{
	    
	    const int sub_x = m_myPlayer.getSubmarine().getX();
        const int sub_y = m_myPlayer.getSubmarine().getY();
        
		for (int dx = -4; dx < 5; dx++)
		{
			for (int dy = -4; dy < 5; dy++)
			{
			    if (abs(dx) + abs(dy) >= 2 && abs(dx) + abs(dy) <= 4)
			    {
			        if (m_oppFinder.canBeOpp(sub_x + dx, sub_y + dy))
    				{
    					shootTorpedo(sub_x + dx, sub_y + dy);
    					return true;
    				}
			    }
			}
		}
		
		return false;
	}
	
	bool goTo(const Point& target, bool secondAction=false)
	{
	    cerr << "Go to " << target.x << " " << target.y << endl;
		const int sub_x = m_myPlayer.getSubmarine().getX();
        const int sub_y = m_myPlayer.getSubmarine().getY();
		
		const Point directionPoint = Point(target.x - sub_x, target.y - sub_y);
		
		array<Delta, 4> bestDirection;
		
		// très surement factorisable mais la flemme
		if (abs(directionPoint.x) > abs(directionPoint.y))
		{
			if (directionPoint.x < 0)
			{
				bestDirection[0] = Delta(-1, 0);
				bestDirection[3] = Delta(1, 0);
			}
			else
			{
				bestDirection[0] = Delta(1, 0);
				bestDirection[3] = Delta(-1, 0);
			}
			
			if (directionPoint.y < 0)
			{
				bestDirection[1] = Delta(0, -1);
				bestDirection[2] = Delta(0, 1);
			}
			else
			{
				bestDirection[1] = Delta(0, 1);
				bestDirection[2] = Delta(0, -1);
			}
		}		
		else
		{
			if (directionPoint.y < 0)
			{
				bestDirection[0] = Delta(0, -1);
				bestDirection[3] = Delta(0, 1);
			}
			else
			{
				bestDirection[0] = Delta(0, 1);
				bestDirection[3] = Delta(0, -1);
			}
			
			if (directionPoint.x < 0)
			{
				bestDirection[1] = Delta(-1, 0);
				bestDirection[2] = Delta(1, 0);
			}
			else
			{
				bestDirection[1] = Delta(1, 0);
				bestDirection[2] = Delta(-1, 0);
			}
		}
		
		for (int i = 0; i < 4; i++)
		{
			if (m_moveMap->isMovable(sub_x + bestDirection[i].x, sub_y + bestDirection[i].y))
			{
			    if (secondAction)
			        newAction();
				move(delta2direction(bestDirection[i]));
				chargeTorpedo();
				
				return true;
			}
		}
		
		// not direction allowed		
		return false;
	}
	
	void doSomething()
	{
	    bool fireTorpedo = false;
	    if (m_myPlayer.getSubmarine().canShootTorpedo())
		{
			fireTorpedo = findAndAttack();
		}
		
		bool moved = false;
    	const Point barycenter = m_oppFinder.getBarycenter();
    		
    	moved = goTo(barycenter, fireTorpedo);
		
		if (!fireTorpedo && !moved)
		    surface();

		endAction();
		return;
	}
    
    void moveAttackRandom()
    {
		const int sub_x = m_myPlayer.getSubmarine().getX();
        const int sub_y = m_myPlayer.getSubmarine().getY();
		
		if (m_myPlayer.getSubmarine().canShootTorpedo())
		{
			findAndAttack();
		}
		
        const array<int, 4> dx = { -1, 0, 1, 0 };
        const array<int, 4> dy = { 0, -1, 0, 1 };
        
        int direction_idx = 0;
        for (; direction_idx < 4; direction_idx++)
        {
            if (m_moveMap->isMovable(sub_x + dx[direction_idx], sub_y + dy[direction_idx]))
            {
                break;
            }
        }

        switch (direction_idx)
        {
            case 0:
                move(Direction::kWest);
                break;
            case 1:
                move(Direction::kNorth);
                break;
            case 2:
                move(Direction::kEast);
                break;
            case 3:
                move(Direction::kSouth);
                break;
            case 4:
                surface();
                break;
        }
        
        if (direction_idx < 4)
        {
            chargeTorpedo();
        }
        endAction();
    }     
};

/*
/* ####################################
/* main
/* ####################################
*/

int main()
{
    MoveMap moveMap;
    
    int width;
    int height;
    int myId;
    cin >> width >> height >> myId; cin.ignore();
    for (int i = 0; i < height; i++) {
        string line;
        getline(cin, line);
        for (int x = 0; x < height; x++)
        {
            if (line[x] == 'x')
                moveMap.setIsland(x, i);
        }
    }
    
    OppFinder oppFinder(moveMap);
    
    Player myPlayer(myId);
    
    const int oppId = (myId == 0) ? 1 : 0;
    Player oppPlayer(oppId);

    // Write an action using cout. DON'T FORGET THE "<< endl"
    // To debug: cerr << "Debug messages..." << endl;

    moveMap.getInitialPosition();

    // game loop
    while (1) {
        int x;
        int y;
        int myLife;
        int oppLife;
        int torpedoCooldown;
        int sonarCooldown;
        int silenceCooldown;
        int mineCooldown;
        cin >> x >> y >> myLife >> oppLife >> torpedoCooldown >> sonarCooldown >> silenceCooldown >> mineCooldown; cin.ignore();
        string sonarResult;
        cin >> sonarResult; cin.ignore();
        string opponentOrders;
        getline(cin, opponentOrders);
        
        moveMap.setPath(x, y);
        
        myPlayer.setLife(myLife);
        myPlayer.setSubmarine(x, y, torpedoCooldown);
        
        oppPlayer.setLife(oppLife);
        
        const size_t foundMove = opponentOrders.find("MOVE");
        if (foundMove != string::npos)
        {
            int dx = 0;
            int dy = 0;
            switch(opponentOrders[foundMove + 5])
            {
               case 'N':
                    dy = -1;
                    break;
                case 'W':
                    dx = -1;
                    break;
                case 'S':
                    dy = 1;
                    break;
                case 'E':
                    dx = 1;
                    break;                    
            };

            oppFinder.update(dx, dy);
        }
        oppFinder.print();
        //myPlayer.print();
        Game game(myPlayer, oppPlayer, &moveMap, oppFinder);
        game.doSomething();

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;

        //cout << "MOVE N TORPEDO" << endl;
    }
}