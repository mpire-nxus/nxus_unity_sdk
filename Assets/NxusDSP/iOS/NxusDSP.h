//
//  NxusDSP.h
//  NxusDSP
//
//  Copyright © 2016. TechMpire ltd. All rights reserved.
//

#import <Foundation/Foundation.h>

/**
 * The main interface to NxusDSP.
 * Use the methods of this class to tell NxusDSP about the usage of your app.
 */
@interface NxusDSP : NSObject

+(void) setSdkPlatform:(NSString *)platform;
+ (void) debuggingEnabled:(BOOL)enabled;
+(void)initializeLibrary:(NSString *)dspApiKey;
-(id)initWithApiKey:(NSString *)apiKey;
+(void)trackEvent:(NSString *)event;
+(void)trackEvent:(NSString *)event params:(NSMutableDictionary *)params;

@end
