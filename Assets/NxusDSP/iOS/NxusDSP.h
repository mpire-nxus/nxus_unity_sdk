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
+(void)trackEventInstall:(NSMutableDictionary *)params;
+(void)trackEventOpen:(NSMutableDictionary *)params;
+(void)trackEventRegistration:(NSMutableDictionary *)params;
+(void)trackEventPurchase:(NSMutableDictionary *)params;
+(void)trackEventLevel:(NSMutableDictionary *)params;
+(void)trackEventTutorial:(NSMutableDictionary *)params;
+(void)trackEventAddToCart:(NSMutableDictionary *)params;
+(void)trackEventCheckout:(NSMutableDictionary *)params;
+(void)trackEventInvite:(NSMutableDictionary *)params;
+(void)trackEventAchievement:(NSMutableDictionary *)params;

@end
