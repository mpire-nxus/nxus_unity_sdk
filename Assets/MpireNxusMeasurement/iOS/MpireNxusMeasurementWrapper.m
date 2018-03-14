//
//  MpireNxusMeasurementWrapper.m
//

#import "MpireNxusMeasurement.h"
#import "MpireNxusMeasurementWrapper.h"

@implementation MpireNxusMeasurementWrapper

void mpire_nxus_measurement_set_sdk_platform(char *platform) {
    [MpireNxusMeasurement setSdkPlatform:[NSString stringWithUTF8String:platform]];
}

void mpire_nxus_measurement_debugging_enabled(bool *enabled) {
    [MpireNxusMeasurement debuggingEnabled:enabled];
}
    
void mpire_nxus_measurement_initialize_library(char *dsp_api_key) {
    [MpireNxusMeasurement initializeLibrary:[NSString stringWithUTF8String:dsp_api_key]];
}
    
void mpire_nxus_measurement_track_event(char *eventName) {
    [MpireNxusMeasurement trackEvent:[NSString stringWithUTF8String:eventName]];
}

void mpire_nxus_measurement_track_event_with_params(char *eventName, const char *attributes) {
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
    [MpireNxusMeasurement trackEvent:[NSString stringWithUTF8String:eventName] params:oAttributes];
}

void mpire_nxus_measurement_track_event_install(const char *attributes) {
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
    [MpireNxusMeasurement trackEventInstall:oAttributes];
}

void mpire_nxus_measurement_track_event_open(const char *attributes) {
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
    [MpireNxusMeasurement trackEventOpen:oAttributes];
}

void mpire_nxus_measurement_track_event_registration(const char *attributes) {
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
    [MpireNxusMeasurement trackEventRegistration:oAttributes];
}

void mpire_nxus_measurement_track_event_purchase(const char *attributes) {
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
    [MpireNxusMeasurement trackEventPurchase:oAttributes];
}

void mpire_nxus_measurement_track_event_level(const char *attributes) {
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
    [MpireNxusMeasurement trackEventLevel:oAttributes];
}

void mpire_nxus_measurement_track_event_tutorial(const char *attributes) {
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
    [MpireNxusMeasurement trackEventTutorial:oAttributes];
}

void mpire_nxus_measurement_track_event_add_to_cart(const char *attributes) {
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
    [MpireNxusMeasurement trackEventAddToCart:oAttributes];
}

void mpire_nxus_measurement_track_event_checkout(const char *attributes) {
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
    [MpireNxusMeasurement trackEventCheckout:oAttributes];
}

void mpire_nxus_measurement_track_event_invite(const char *attributes) {
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
    [MpireNxusMeasurement trackEventInvite:oAttributes];
}

void mpire_nxus_measurement_track_event_achievement(const char *attributes) {
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
    [MpireNxusMeasurement trackEventAchievement:oAttributes];
}

@end
