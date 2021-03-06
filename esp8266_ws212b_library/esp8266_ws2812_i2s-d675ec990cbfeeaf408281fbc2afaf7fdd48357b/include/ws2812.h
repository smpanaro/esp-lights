// ws2812.h
// This file MUST be present in your project folder, i.e. where
// the .ino file is located...it's used by the ws2812_lib 
// 

#ifndef __WS2812_H__
#define __WS2812_H__

#define WS2812_GAMMA_CORRECTION (1)         // 0 = off, 1=on (I might change this in the near
                                            // future to support different gamma curves) 
#define WS2812_DITHER_NUM       (8)         // 1, 2, 4, 8  (1 = no dithering)
#define WS2812_USE_INTERRUPT    (0)         // not supported yet


#endif

// end of file
