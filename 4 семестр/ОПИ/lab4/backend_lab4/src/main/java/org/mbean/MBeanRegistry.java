package org.mbean;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.ejb.Singleton;
import jakarta.ejb.Startup;
import jakarta.inject.Inject;
import javax.management.MBeanServer;
import javax.management.ObjectName;
import javax.management.StandardMBean;

import org.mbean.interfaces.AreaCalculatorMBean;
import org.mbean.interfaces.PointsCounterMBean;

import javax.management.StandardEmitterMBean;
import java.lang.management.ManagementFactory;

@Singleton
@Startup
public class MBeanRegistry {

    @Inject
    private PointsCounter pointsCounter;

    @Inject
    private AreaCalculator areaCalculator;

    private ObjectName pointsCounterName;
    private ObjectName areaCalculatorName;

    @PostConstruct
    public void registerMBeans() {
        try {
            MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
            
            pointsCounterName = new ObjectName("org.mbeans:type=PointsCounter");
            StandardEmitterMBean pointsCounterWrapper = new StandardEmitterMBean(
                pointsCounter, PointsCounterMBean.class, pointsCounter
            );
            mbs.registerMBean(pointsCounterWrapper, pointsCounterName);

            areaCalculatorName = new ObjectName("org.mbeans:type=AreaCalculator");
            StandardMBean areaCalculatorWrapper = new StandardMBean(
                areaCalculator, AreaCalculatorMBean.class
            );
            mbs.registerMBean(areaCalculatorWrapper, areaCalculatorName);
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @PreDestroy
    public void unregisterMBeans() {
        try {
            MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
            if (pointsCounterName != null) mbs.unregisterMBean(pointsCounterName);
            if (areaCalculatorName != null) mbs.unregisterMBean(areaCalculatorName);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}