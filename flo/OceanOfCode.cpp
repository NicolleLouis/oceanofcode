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
        
        if (m_cells[x][y] == CellType::kEmpty)
        {
            return true;
        }
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
};

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
	
	void print() const
	{
		m_oppPositionMap.print();
	}
	
};

class Game
{
private:
    Player m_myPlayer;
    Player m_oppPlayer;
    MoveMap m_moveMap;
	OppFinder m_oppFinder;
    
    enum Direction
    {
        kNorth,
        kEast,
        kSouth,
        kWest
    };
    
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
        cout << "SURFACE" << endl;
        m_moveMap.reset();
    }
    
    void chargeTorpedo() { cout << " TORPEDO"; }
    
    void newAction() { cout << "|"; }
    
    void endAction() { cout << endl; }
    
    
public:
    Game(const Player& myPlayer, const Player& oppPlayer, const MoveMap& moveMap, const OppFinder& oppFinder) :
    m_myPlayer(myPlayer),
    m_oppPlayer(oppPlayer),
    m_moveMap(moveMap),
	m_oppFinder(oppFinder)
    {  
    };
	
	void findAndAttack(const int x, const int y)
	{
		for (int dx = -4; dx < 5; dx++)
		{
			for (int dy = -4; dy < 5; dy++)
			{
				if (oppFinder.canBeOpp(sub_x + dx, sub_y + dy))
				{
					shootTorpedo(sub_x + dx, sub_y + dy);
					newAction();
					return;
				}
			}
		}
	}
    
    void moveAttackRandom()
    {
		const int sub_x = m_myPlayer.getSubmarine().getX();
        const int sub_y = m_myPlayer.getSubmarine().getY();
		
		if (m_myPlayer.getSubmarine().canShootTorpedo())
		{
			findAndAttack(sub_x, sub_y);
		}
		
        const array<int, 4> dx = { -1, 0, 1, 0 };
        const array<int, 4> dy = { 0, -1, 0, 1 };
        
        int direction_idx = 0;
        for (; direction_idx < 4; direction_idx++)
        {
            if (m_moveMap.isMovable(x + dx[direction_idx], y + dy[direction_idx]))
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
        
        chargeTorpedo();
        endAction();
    }     
};


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
        myPlayer.print();
        Game game(myPlayer, oppPlayer, moveMap, oppFinder);
        game.moveAttackRandom();

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;

        //cout << "MOVE N TORPEDO" << endl;
    }
}