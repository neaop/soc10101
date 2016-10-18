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

// sql to read in all the required tables
def getFittsSectorID = """
select * from fittssectorid
where patternref = ?"""

def getFSectorTimes = """SELECT *
FROM fittssectortimes"""

def getFLoopLocations = """Select *
FROM fittslooplocations
where collectionref = ? and
sequenceNo = ?"""

def getFStasisLocations = """Select *
from fittsstasislocations
where collectionref = ? and
sequenceNo = ?"""

def getFLiftLocations = """select *
from fittsliftlocations
where collectionref = ? and
sequenceNo = ?"""

def getPatternPoints = """select *
from patternpoints
where
patternRef = 3 or
patternRef = 4
order by patternRef, xValue
"""

// sql to insert data into fitssvalidsectors
def insertFValidSectors = """
INSERT INTO `schoolsv6`.`fittsvalidsectors`
(`patternRef`,
`sectorNo`,
`timeTaken`,
years,
months,
`collectionRef`,
`sequenceNo`)
VALUES
(?,?,?,?,?,?,?)"""

// extract sector data into  data structures

def fst = sql.rows(getFSectorTimes)
def fsidP3 = sql.rows(getFittsSectorID, [3])
def fsidP4 = sql.rows(getFittsSectorID, [4])

fsidP3.each {println "$it"}
println "\n"
fsidP4.each {println "$it"}
/*
def patternPoints = sql.rows(getPatternPoints)
println "\n"
patternPoints.each{println "$it"}
println "\n"
*/

/* define the concepts of
 * close to a pattern dot
 * between pattern dots
 */
def findClosestDot = { x, y, fsID ->
	// x and y are the coordinates of the point where the lift, stasis or loop occurred
	//fsID is the pattern point table to use
	//TODO modify so it works correctly start with minDistance = 1000 and first dot = [0,100]
	def nDots = fsID.size()
	def minDistance = 1000
	def nextDot = -1 //because first dot missong from fsID
	def nextDotX = 0
	def nextDotY = 100
	def xDiff = Math.abs(nextDotX - x)
	def yDiff = Math.abs(nextDotY - y)
	def nextDistance = Math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
	while ((nextDot < (nDots - 1)) && (nextDistance < minDistance)) {
		minDistance = nextDistance
		nextDot = nextDot + 1
		nextDotX = fsID[nextDot][2]
		nextDotY = fsID[nextDot][3]
		xDiff = Math.abs(nextDotX - x)
		yDiff = Math.abs(nextDotY - y)
		nextDistance = Math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
	}
	return [nextDot, minDistance]
}

def closeBy = {x, y, rx, ry, margin, patternRef ->
	def dotData = (patternRef == 3) ? findClosestDot (x, y, fsidP3) : findClosestDot (x, y, fsidP4) 
	if (dotData[1] <= margin) dotData << "Close" else dotData << "Far"
	return dotData
}

//println "fcp: ${fcp.size()}, loops:  ${loops.size()}, stasis: ${stasis.size()},  lifts: ${lifts.size()}"
println "\nprocessing ${fst.size()} entries"
// iterate through all the collection patterns with fitts data from fittssectortimes
def close = 0
def far = 0
fst.each{ row ->
	int collection = row[0]
	int sequenceNo = row[1]
	int pattern = row[2]
	int year = row[4]
	int month = row[5]
//	println "row: $rowNo - $collection, $sequenceNo, $pattern"
	def loops = sql.rows(getFLoopLocations, [collection, sequenceNo])
	def stasis = sql.rows(getFStasisLocations, [collection, sequenceNo])
	def lifts = sql.rows(getFLiftLocations, [collection, sequenceNo])
//	println "$rowNo: $collection , $sequenceNo [$year|$month]= loops:  ${loops.size()}, stasis: ${stasis.size()},  lifts: ${lifts.size()}"
	rowNo = rowNo + 1
//	loops.each {loop ->
	// process each loop
//	}
	//println "stasis details for ${stasis.size()} rows"
	stasis.each{still ->
		def margin = 20
		def dotData = closeBy(still[3], still[4], 0, 0, margin, still[2])
		if (dotData[2] == "Close") close = close + 1 else far = far + 1
		println "c: ${still[0]}, s: ${still[1]}, p: ${still[2]}, x: ${still[3]}, y: ${still[4]} == dot: ${dotData[0]}, margin: ${dotData[1]}, ${dotData[2]}"
	}
	lifts.each{lift ->

	}
}
int rowNo = 1
println " stasis close patterns = $close, far patterns = $far"

