
import  java.sql.*

public class connect Connect {
	public static void main(String[] args) {
		Connection connect = null;
		String url = "jdbc:mysql://localhost/testdb";
		String userName = "root";
		String password = "123456";

		try{
			Class.forName("com.mysql.jdbc.Driver").newInstance();
			connect = DriverManager.getConnection(url, userName, password )
		             # TODO
		}
	}
}