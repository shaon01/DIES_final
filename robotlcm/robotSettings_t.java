/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 */

package robotlcm;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class robotSettings_t implements lcm.lcm.LCMEncodable
{
    public long timestamp;
    public int desiredSpeed;
    public double positionFromGPS[];
    public boolean changeLane;
 
    public robotSettings_t()
    {
        positionFromGPS = new double[3];
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0x2f6c5eb55b26a404L;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(robotlcm.robotSettings_t.class))
            return 0L;
 
        classes.add(robotlcm.robotSettings_t.class);
        long hash = LCM_FINGERPRINT_BASE
            ;
        classes.remove(classes.size() - 1);
        return (hash<<1) + ((hash>>63)&1);
    }
 
    public void encode(DataOutput outs) throws IOException
    {
        outs.writeLong(LCM_FINGERPRINT);
        _encodeRecursive(outs);
    }
 
    public void _encodeRecursive(DataOutput outs) throws IOException
    {
        outs.writeLong(this.timestamp); 
 
        outs.writeInt(this.desiredSpeed); 
 
        for (int a = 0; a < 3; a++) {
            outs.writeDouble(this.positionFromGPS[a]); 
        }
 
        outs.writeByte( this.changeLane ? 1 : 0); 
 
    }
 
    public robotSettings_t(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public robotSettings_t(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static robotlcm.robotSettings_t _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        robotlcm.robotSettings_t o = new robotlcm.robotSettings_t();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        this.timestamp = ins.readLong();
 
        this.desiredSpeed = ins.readInt();
 
        this.positionFromGPS = new double[(int) 3];
        for (int a = 0; a < 3; a++) {
            this.positionFromGPS[a] = ins.readDouble();
        }
 
        this.changeLane = ins.readByte()!=0;
 
    }
 
    public robotlcm.robotSettings_t copy()
    {
        robotlcm.robotSettings_t outobj = new robotlcm.robotSettings_t();
        outobj.timestamp = this.timestamp;
 
        outobj.desiredSpeed = this.desiredSpeed;
 
        outobj.positionFromGPS = new double[(int) 3];
        System.arraycopy(this.positionFromGPS, 0, outobj.positionFromGPS, 0, 3); 
        outobj.changeLane = this.changeLane;
 
        return outobj;
    }
 
}

