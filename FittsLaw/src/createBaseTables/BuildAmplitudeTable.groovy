package createBaseTables

import candid.ConnectDB
import phw.util.*

//def DBname = Ask.string ("Please input the name of the Database you want to use: ")
def DBname = "schoolsv6"
def domain = "localhost"
def UserName = "root"
def PassWord = "admin"

def connection = new ConnectDB(domain, DBname, UserName, PassWord)
def sql = connection.getConnection()

println "Connection made to MySQL $DBname"

def selectPatternPoints = """
SELECT * FROM patternPoints
where patternRef = ?"""

def insertfittssectorid = """
INSERT INTO `schoolsv6`.`fittssectorid`
(`patternRef`,
`sectorNo`,
`patternX`,
`patternY`,
`FittsID`,
`lineDirection`)
VALUES (?,?,?,?,?,?)"""

int margin = 7	// area around target pixel which is considered part of the target
				// a radius in pixels (halfway between dot and total target area radius
double width = 20.0	// diameter of total target area in pixels as a double

double log2 = Math.log(2)

for ( patternRef in 3..4){
	def patternPoints = sql.rows(selectPatternPoints,patternRef)
//	patternPoints.each {row ->
//		println "${row[0]}, ${row[1]}, ${row[2]} "		
//	}
	int patternSize = patternPoints.size()
	for ( p in 1..patternSize - 1){
		int direction = (patternPoints[p-1][2] <=> patternPoints[p][2])
		// direction = 1 if line joining points goes up
		//			 = 0 if line is horizontal
		//			 = -1 if line joining points goes down
		int xDiff = Math.abs(patternPoints[p][1] - patternPoints[p-1][1]) - margin
		int yDiff = Math.abs(patternPoints[p][2] - patternPoints[p-1][2]) - margin
		double amplitude = Math.sqrt(xDiff * xDiff + yDiff * yDiff)
		double twoAdivW = 2 * amplitude / width
		double ID = Math.log(twoAdivW) / log2
		println "${patternPoints[p][0]}, $p, ${patternPoints[p][1]}, ${patternPoints[p][2]}, $xDiff, $yDiff, $amplitude, $twoAdivW, $ID, $direction "
		sql.execute(insertfittssectorid, [patternPoints[p][0], p, patternPoints[p][1], patternPoints[p][2], ID, direction])
	}
}
