// generated from a.proto by py-protoc, NEVER CHANGE!!

#import "XG_BaseModel.h"
#import "BPBenum.h"
@class APAmsg2;

/**
 * a1
a2
 */
@interface APAmsg1 : XG_BaseModel
/**
 * str前的注释
 */
@property(nonatomic, strong) NSString * str;
/**
 * int32后的注释
 */
@property(nonatomic, strong) NSNumber * int_32;
/**
 * int64前的注释1
int64后的注释2
 */
@property(nonatomic, strong) NSNumber * int_64;
@property(nonatomic, strong) NSNumber * float_;
@property(nonatomic, strong) NSNumber * double_;
@property(nonatomic, strong) NSNumber * bool_;
@property(nonatomic, assign) BPBenum b_enum;
@property(nonatomic, strong) APAmsg2 * amsg2;
@property(nonatomic, strong) NSMutableArray * amsg2_list;
@property(nonatomic, strong) NSMutableArray * str_list;
@property(nonatomic, strong) NSMutableArray * benum_list;
@property(nonatomic, strong) NSMutableDictionary * int_map;
@property(nonatomic, strong) NSMutableDictionary * amsg2_map;
@property(nonatomic, strong) NSString * byte_str;
@end

