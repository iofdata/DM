package com.tanhao.test;

abstract class Father{
	static  String famliyname = "James";
	private String name = null;
	private int age = 40;
	private static int test;
	
	/*
	public Father(){}
	
	public Father(String name,int age){
		this.name = name;
		this.age = age;
	}
	*/
	
	public String getName() {
		return name;
	}
	
	final public void setName(String name) {
		this.name = name;
	}
	
	//protected abstract void setName(String name);
	
	public void setAge(int age) {
		this.age = age;
	}

	public int getAge() {
		return age;
	}

	protected abstract void dosth();
	
	protected void printname(){
		System.out.println("famliyname:" + famliyname);
		System.out.println("name:" + this.name);
		System.out.println("age:" + this.age);
		System.out.println("test:" + Father.getTest());
	}
	
	final void run(){
		dosth();
		printname();
	}

	public static int getTest() {
		return test;
	}

	public static void setTest(int test) {
		Father.test = test;
	}
}

class SonA extends Father{
	/*
	public SonA(String name,int age){
		super(name,age);
	}
	*/
	
	@Override
	protected void dosth() {
		// TODO Auto-generated method stub
		System.out.println("I am Son A!");
		//SonA.setName("Jack");
		//SonA.setAge(20);
		SonA.setTest(30);	
	}
}

class SonB extends Father{
	/*
	public SonB(String name,int age){
		super(name,age);
	}
	*/

	@Override
	protected void dosth() {
		// TODO Auto-generated method stub
		System.out.println("I am Son B!");
		//SonB.setName("Jim");
		//SonB.setAge(30);
		SonB.setTest(20);	
	}	
}

class SonC extends Father{
	public SonC(){
		super();
	}
	
	/*
	public SonC(String name,int age){
		super(name,age);
	}
	*/

	@Override
	protected void dosth() {
		// TODO Auto-generated method stub
		System.out.println("I am Son C!");
		//SonC.setName("Json");
		//SonC.setAge(30);
		//SonC.setTest(20);	
	}	
}

class Test{
	public static void main(String args[]){
		Father sonA = new SonA();
		sonA.setName("Jim");
		sonA.setAge(30);
		sonA.run();
		Father sonB = new SonB();
		sonB.run();
		Father sonC = new SonC();
		sonC.run();
		
		System.out.println("######");
		
		SonA sonA1 = new SonA();
		sonA1.setName("Jim");
		sonA1.setAge(30);
		sonA1.run();
		SonB sonB1 = new SonB();
		sonB1.run();
		SonC sonC1 = new SonC();
		sonC1.run();
		
	}
}
