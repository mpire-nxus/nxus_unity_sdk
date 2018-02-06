//
//  NxusDSPWrapper.m
//  
//
//  Created by Tomislav Tusek on 12/09/16.
//
//

#import "NxusDSP.h"
#import "NxusDSPWrapper.h"

@implementation NxusDSPWrapper

void nxus_dsp_set_sdk_platform(char *platform) {
    [NxusDSP setSdkPlatform:[NSString stringWithUTF8String:platform]];
}

void nxus_dsp_debugging_enabled(bool *enabled) {
    [NxusDSP debuggingEnabled:enabled];
}
    
void nxus_dsp_initialize_library(char *dsp_api_key) {
    [NxusDSP initializeLibrary:[NSString stringWithUTF8String:dsp_api_key]];
}
    
void nxus_dsp_track_event(char *eventName) {
    [NxusDSP trackEvent:[NSString stringWithUTF8String:eventName]];
}

void nxus_dsp_track_event_with_params(char *eventName, const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEvent:[NSString stringWithUTF8String:eventName] params:oAttributes];
}

void nxus_dsp_track_event_install(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventInstall:oAttributes];
}

void nxus_dsp_track_event_open(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventOpen:oAttributes];
}

void nxus_dsp_track_event_registration(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventRegistration:oAttributes];
}

void nxus_dsp_track_event_purchase(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventPurchase:oAttributes];
}

void nxus_dsp_track_event_level(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventLevel:oAttributes];
}

void nxus_dsp_track_event_tutorial(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventTutorial:oAttributes];
}

void nxus_dsp_track_event_add_to_cart(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventAddToCart:oAttributes];
}

void nxus_dsp_track_event_checkout(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventCheckout:oAttributes];
}

void nxus_dsp_track_event_invite(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventInvite:oAttributes];
}

void nxus_dsp_track_event_achievement(const char *attributes) {
    NSString *attris = [NSString stringWithUTF8String:attributes];
    NSArray *attributesArray = [attris componentsSeparatedByString:@"\n"];
    
    NSMutableDictionary *oAttributes = [[NSMutableDictionary alloc] init];
    for (int i = 0; i < [attributesArray count]; i++) {
        NSString *keyValuePair = [attributesArray objectAtIndex:i];
        NSRange range = [keyValuePair rangeOfString:@"="];
        if (range.location != NSNotFound) {
            NSString *key = [keyValuePair substringToIndex:range.location];
            NSString *value = [keyValuePair substringFromIndex:range.location+1];
            [oAttributes setObject:value forKey:key];
        }
    }
    [NxusDSP trackEventAchievement:oAttributes];
}

@end
