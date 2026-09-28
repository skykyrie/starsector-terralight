package org.lwjgl.util.vector;
public class Vector2f implements ReadableVector2f { public float x,y;
 public Vector2f(){} public Vector2f(float x,float y){this.x=x;this.y=y;} public Vector2f(ReadableVector2f o){x=o.getX();y=o.getY();}
 public float getX(){return x;} public float getY(){return y;} public void setX(float v){x=v;} public void setY(float v){y=v;}
 public Vector2f set(float a,float b){x=a;y=b;return this;} public Vector2f set(ReadableVector2f o){x=o.getX();y=o.getY();return this;}
 public float length(){return (float)Math.sqrt(x*x+y*y);} public float lengthSquared(){return x*x+y*y;}
 public Vector2f scale(float s){x*=s;y*=s;return this;} public Vector2f negate(){x=-x;y=-y;return this;} public Vector2f negate(Vector2f d){return d;}
 public Vector2f normalise(){return this;} public Vector2f normalise(Vector2f d){return d;} public Vector2f translate(float a,float b){x+=a;y+=b;return this;}
 public static Vector2f add(Vector2f a,Vector2f b,Vector2f d){return d;} public static Vector2f sub(Vector2f a,Vector2f b,Vector2f d){return d;}
 public static float dot(Vector2f a,Vector2f b){return 0;} public static float angle(Vector2f a,Vector2f b){return 0;} }