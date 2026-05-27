package org;

import org.utils.AreaChecker;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AreaHitTest {
    @Nested
    @DisplayName("1-я четверть: Пустая область")
    class FirstQuadrantTests {
        @ParameterizedTest
        @CsvSource({
            "1.0,  1.0, 2.0, false",
            "0.1,  0.1, 2.0, false",
            "5.0,  5.0, 2.0, false"
        })
        void testEmptyArea(double x, double y, double r, boolean expected) {
            assertEquals(expected, AreaChecker.checkArea(x, y, r));
        }
    }

    @Nested
    @DisplayName("2-я четверть: окружность R/2")
    class SecondQuadrantTests {
        @ParameterizedTest
        @CsvSource({
            " 0.0,  1.0, 2.0, true",   
            "-1.0,  0.0, 2.0, true",   
            "-0.5,  0.5, 2.0, true",   
            "-1.0,  1.0, 2.0, false",  
            "-0.1,  1.1, 2.0, false"   
        })
        void testCircleArea(double x, double y, double r, boolean expected) {
            assertEquals(expected, AreaChecker.checkArea(x, y, r));
        }
    }

    @Nested
    @DisplayName("3-я четверть: треугольник ")
    class ThirdQuadrantTests {
        @ParameterizedTest
        @CsvSource({
            " 0.0, -2.0, 2.0, true",   
            "-2.0,  0.0, 2.0, false",   
            "-1.0, -1.0, 2.0, true",   
            "-0.5, -0.5, 2.0, true",   
            "-1.5, -1.5, 2.0, false",  
            "-2.1, -0.1, 2.0, false"   
        })
        void testTriangleArea(double x, double y, double r, boolean expected) {
            assertEquals(expected, AreaChecker.checkArea(x, y, r));
        }
    }

    @Nested
    @DisplayName("4-я четверть: Прямоугольник")
    class FourthQuadrantTests {
        @ParameterizedTest
        @CsvSource({
            " 0.0,  0.0, 2.0, true",   
            " 2.0,  0.0, 2.0, true",   
            " 0.0, -2.0, 2.0, true",   
            " 2.0, -2.0, 2.0, true",   
            " 1.0, -1.0, 2.0, true",   
            " 2.5, -1.0, 2.0, false",  
            " 1.0, -2.5, 2.0, false"   
        })
        void testRectangleArea(double x, double y, double r, boolean expected) {
            assertEquals(expected, AreaChecker.checkArea(x, y, r));
        }
    }
}