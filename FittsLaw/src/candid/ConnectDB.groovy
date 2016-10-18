package candid

import groovy.sql.*

class ConnectDB {
	def domain, DBname, user, password, sql
	
	def ConnectDB (domain, DBname, user, password){
		this.domain = domain
		this.DBname = DBname
		this.user = user
		this.password = password
		def driver = "com.mysql.jdbc.Driver"
		def DB = "jdbc:mysql://" + domain + ":3306/"+ DBname		
		sql = Sql.newInstance(DB, user, password, driver)
		def useCommand = "USE `" + DBname + "`" 
		//println "about to do USE"
		sql.execute(useCommand)
		println "$useCommand"
	}
	def getConnection(){
		return sql
	}
}
