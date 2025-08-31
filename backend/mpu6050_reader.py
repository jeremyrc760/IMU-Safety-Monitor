
#!/usr/bin/env python3
import os, time, json
from datetime import datetime
from smbus2 import SMBus
import requests

I2C_BUS = 1
MPU_ADDR = 0x68
API_BASE = os.environ.get("API_BASE", "")
POST_INTERVAL_SEC = 0.5
READ_HZ = 50

PWR_MGMT_1=0x6B; ACCEL_XOUT_H=0x3B
ACCEL_SENS=16384.0; GYRO_SENS=131.0; G=9.80665

def _twos16(v): return v-0x10000 if v & 0x8000 else v

class MPU6050:
    def __init__(self, bus, addr):
        self.bus=bus; self.addr=addr
        self.bus.write_byte_data(self.addr, PWR_MGMT_1, 0)
        time.sleep(0.05)
    def read(self):
        d=self.bus.read_i2c_block_data(self.addr, ACCEL_XOUT_H, 14)
        ax=_twos16((d[0]<<8)|d[1])/ACCEL_SENS*G
        ay=_twos16((d[2]<<8)|d[3])/ACCEL_SENS*G
        az=_twos16((d[4]<<8)|d[5])/ACCEL_SENS*G
        gx=_twos16((d[8]<<8)|d[9])/GYRO_SENS
        gy=_twos16((d[10]<<8)|d[11])/GYRO_SENS
        gz=_twos16((d[12]<<8)|d[13])/GYRO_SENS
        return ax,ay,az,gx,gy,gz

def main():
    period=1.0/READ_HZ; last=0
    with SMBus(I2C_BUS) as bus:
        m=MPU6050(bus,MPU_ADDR)
        while True:
            t0=time.time()
            ax,ay,az,gx,gy,gz=m.read()
            payload={"ax":ax,"ay":ay,"az":az,"gx":gx,"gy":gy,"gz":gz,"ts":datetime.utcnow().isoformat()+"Z"}
            print(json.dumps(payload))
            if API_BASE and (t0-last)>=POST_INTERVAL_SEC:
                try: requests.post(API_BASE.rstrip('/')+'/api/imu',json=payload,timeout=2)
                except: pass
                last=t0
            dt=time.time()-t0
            if dt<period: time.sleep(period-dt)

if __name__=="__main__": main()
