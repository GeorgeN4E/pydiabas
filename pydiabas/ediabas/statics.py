# Import ctypes and enum
import ctypes
import enum

# Typedefs from Api.h
API_CHAR = ctypes.c_char
API_TEXT = ctypes.c_char
API_BYTE = ctypes.c_ubyte
API_BINARY = ctypes.c_ubyte
API_INTEGER = ctypes.c_short
API_WORD = ctypes.c_ushort
API_LONG = ctypes.c_long
API_DWORD = ctypes.c_ulong
API_REAL = ctypes.c_double


# CONSTANTS from Api.h
API_COMPATIBILITY_VERSION = 0x0700  # API compatibility version
API_MAX_DEVICE = 64  # maximal device incl. '\0'
API_MAX_NAME = 64  # maximal name length incl. '\0'
API_MAX_PARA = 1024  # maximal job para length
API_MAX_PARAEXT = 65536  # maximal job para length / v7
API_MAX_STDPARA = 256  # maximal standard job para length
API_MAX_RESULT = 256  # maximal result length incl. '\0'
API_MAX_TEXT = 1024  # maximal text length incl. '\0'
API_MAX_BINARY = 1024  # maximal binary buffer length
API_MAX_BINARYEXT = 65536  # maximal binary buffer length / v7
API_MAX_CONFIG = 256  # maximal config buffer length incl.'\0'
API_MAX_FILENAME = 256  # maximal file name length incl.'\0'


# API States translations
class API_STATE(enum.IntEnum):
    BUSY = 0
    READY = 1
    BREAK = 2
    ERROR = 3


# API result format translations
class API_RESULT_FORMAT(enum.IntEnum):
    CHAR = 0
    BYTE = 1
    INTEGER = 2
    WORD = 3
    LONG = 4
    DWORD = 5
    TEXT = 6
    BINARY = 7
    REAL = 8


# APIBOOL implementation
class API_BOOL(enum.IntEnum):
    FALSE = 0
    TRUE = 1


# API error code translations
class EDIABAS_ERROR(enum.IntEnum):    
    ERR_NONE = 0
    RESERVED = 1
    ERROR_CODE_OUT_OF_RANGE = 2

    IFH_0000 = 10
    IFH_0001 = 11
    IFH_0002 = 12
    IFH_0003 = 13
    IFH_0004 = 14
    IFH_0005 = 15
    IFH_0006 = 16
    IFH_0007 = 17
    IFH_0008 = 18
    IFH_0009 = 19
    IFH_0010 = 20
    IFH_0011 = 21
    IFH_0012 = 22
    IFH_0013 = 23
    IFH_0014 = 24
    IFH_0015 = 25
    IFH_0016 = 26
    IFH_0017 = 27
    IFH_0018 = 28
    IFH_0019 = 29
    IFH_0020 = 30
    IFH_0021 = 31
    IFH_0022 = 32
    IFH_0023 = 33
    IFH_0024 = 34
    IFH_0025 = 35
    IFH_0026 = 36
    IFH_0027 = 37
    IFH_0028 = 38
    IFH_0029 = 39
    IFH_0030 = 40
    IFH_0031 = 41
    IFH_0032 = 42
    IFH_0033 = 43
    IFH_0034 = 44
    IFH_0035 = 45
    IFH_0036 = 46
    IFH_0037 = 47
    IFH_0038 = 48
    IFH_0039 = 49
    IFH_0040 = 50
    IFH_0041 = 51
    IFH_0042 = 52
    IFH_0043 = 53
    IFH_0044 = 54
    IFH_0045 = 55
    IFH_0046 = 56
    IFH_0047 = 57
    IFH_0048 = 58
    IFH_0049 = 59
    IFH_LAST = IFH_0049

    BIP_0000 = 60
    BIP_0001 = 61
    BIP_0002 = 62
    BIP_0003 = 63
    BIP_0004 = 64
    BIP_0005 = 65
    BIP_0006 = 66
    BIP_0007 = 67
    BIP_0008 = 68
    BIP_0009 = 69
    BIP_0010 = 70
    BIP_0011 = 71
    BIP_0012 = 72
    BIP_0013 = 73
    BIP_0014 = 74
    BIP_0015 = 75
    BIP_0016 = 76
    BIP_0017 = 77
    BIP_0018 = 78
    BIP_0019 = 79
    BIP_0020 = 80
    BIP_0021 = 81
    BIP_0022 = 82
    BIP_0023 = 83
    BIP_0024 = 84
    BIP_0025 = 85
    BIP_0026 = 86
    BIP_0027 = 87
    BIP_0028 = 88
    BIP_0029 = 89
    BIP_LAST = BIP_0029

    SYS_0000 = 90
    SYS_0001 = 91
    SYS_0002 = 92
    SYS_0003 = 93
    SYS_0004 = 94
    SYS_0005 = 95
    SYS_0006 = 96
    SYS_0007 = 97
    SYS_0008 = 98
    SYS_0009 = 99
    SYS_0010 = 100
    SYS_0011 = 101
    SYS_0012 = 102
    SYS_0013 = 103
    SYS_0014 = 104
    SYS_0015 = 105
    SYS_0016 = 106
    SYS_0017 = 107
    SYS_0018 = 108
    SYS_0019 = 109
    SYS_0020 = 110
    SYS_0021 = 111
    SYS_0022 = 112
    SYS_0023 = 113
    SYS_0024 = 114
    SYS_0025 = 115
    SYS_0026 = 116
    SYS_0027 = 117
    SYS_0028 = 118
    SYS_0029 = 119
    SYS_LAST = SYS_0029

    API_0000 = 120
    API_0001 = 121
    API_0002 = 122
    API_0003 = 123
    API_0004 = 124
    API_0005 = 125
    API_0006 = 126
    API_0007 = 127
    API_0008 = 128
    API_0009 = 129
    API_0010 = 130
    API_0011 = 131
    API_0012 = 132
    API_0013 = 133
    API_0014 = 134
    API_0015 = 135
    API_0016 = 136
    API_0017 = 137
    API_0018 = 138
    API_0019 = 139
    API_0020 = 140
    API_0021 = 141
    API_0022 = 142
    API_0023 = 143
    API_0024 = 144
    API_0025 = 145
    API_0026 = 146
    API_0027 = 147
    API_0028 = 148
    API_0029 = 149
    API_LAST = API_0029

    NET_0000 = 150
    NET_0001 = 151
    NET_0002 = 152
    NET_0003 = 153
    NET_0004 = 154
    NET_0005 = 155
    NET_0006 = 156
    NET_0007 = 157
    NET_0008 = 158
    NET_0009 = 159
    NET_0010 = 160
    NET_0011 = 161
    NET_0012 = 162
    NET_0013 = 163
    NET_0014 = 164
    NET_0015 = 165
    NET_0016 = 166
    NET_0017 = 167
    NET_0018 = 168
    NET_0019 = 169
    NET_0020 = 170
    NET_0021 = 171
    NET_0022 = 172
    NET_0023 = 173
    NET_0024 = 174
    NET_0025 = 175
    NET_0026 = 176
    NET_0027 = 177
    NET_0028 = 178
    NET_0029 = 179
    NET_0030 = 180
    NET_0031 = 181
    NET_0032 = 182
    NET_0033 = 183
    NET_0034 = 184
    NET_0035 = 185
    NET_0036 = 186
    NET_0037 = 187
    NET_0038 = 188
    NET_0039 = 189
    NET_0040 = 190
    NET_0041 = 191
    NET_0042 = 192
    NET_0043 = 193
    NET_0044 = 194
    NET_0045 = 195
    NET_0046 = 196
    NET_0047 = 197
    NET_0048 = 198
    NET_0049 = 199
    NET_LAST = NET_0049

    IFH_0050 = 200
    IFH_0051 = 201
    IFH_0052 = 202
    IFH_0053 = 203
    IFH_0054 = 204
    IFH_0055 = 205
    IFH_0056 = 206
    IFH_0057 = 207
    IFH_0058 = 208
    IFH_0059 = 209
    IFH_0060 = 210
    IFH_0061 = 211
    IFH_0062 = 212
    IFH_0063 = 213
    IFH_0064 = 214
    IFH_0065 = 215
    IFH_0066 = 216
    IFH_0067 = 217
    IFH_0068 = 218
    IFH_0069 = 219
    IFH_0070 = 220
    IFH_0071 = 221
    IFH_0072 = 222
    IFH_0073 = 223
    IFH_0074 = 224
    IFH_0075 = 225
    IFH_0076 = 226
    IFH_0077 = 227
    IFH_0078 = 228
    IFH_0079 = 229
    IFH_0080 = 230
    IFH_0081 = 231
    IFH_0082 = 232
    IFH_0083 = 233
    IFH_0084 = 234
    IFH_0085 = 235
    IFH_0086 = 236
    IFH_0087 = 237
    IFH_0088 = 238
    IFH_0089 = 239
    IFH_0090 = 240
    IFH_0091 = 241
    IFH_0092 = 242
    IFH_0093 = 243
    IFH_0094 = 244
    IFH_0095 = 245
    IFH_0096 = 246
    IFH_0097 = 247
    IFH_0098 = 248
    IFH_0099 = 249
    IFH_LAST2 = IFH_0099

    RUN_0000 = 250
    RUN_0001 = 251
    RUN_0002 = 252
    RUN_0003 = 253
    RUN_0004 = 254
    RUN_0005 = 255
    RUN_0006 = 256
    RUN_0007 = 257
    RUN_0008 = 258
    RUN_0009 = 259
    RUN_0010 = 260
    RUN_0011 = 261
    RUN_0012 = 262
    RUN_0013 = 263
    RUN_0014 = 264
    RUN_0015 = 265
    RUN_0016 = 266
    RUN_0017 = 267
    RUN_0018 = 268
    RUN_0019 = 269
    RUN_0020 = 270
    RUN_0021 = 271
    RUN_0022 = 272
    RUN_0023 = 273
    RUN_0024 = 274
    RUN_0025 = 275
    RUN_0026 = 276
    RUN_0027 = 277
    RUN_0028 = 278
    RUN_0029 = 279
    RUN_0030 = 280
    RUN_0031 = 281
    RUN_0032 = 282
    RUN_0033 = 283
    RUN_0034 = 284
    RUN_0035 = 285
    RUN_0036 = 286
    RUN_0037 = 287
    RUN_0038 = 288
    RUN_0039 = 289
    RUN_0040 = 290
    RUN_0041 = 291
    RUN_0042 = 292
    RUN_0043 = 293
    RUN_0044 = 294
    RUN_0045 = 295
    RUN_0046 = 296
    RUN_0047 = 297
    RUN_0048 = 298
    RUN_0049 = 299
    RUN_0050 = 300
    RUN_0051 = 301
    RUN_0052 = 302
    RUN_0053 = 303
    RUN_0054 = 304
    RUN_0055 = 305
    RUN_0056 = 306
    RUN_0057 = 307
    RUN_0058 = 308
    RUN_0059 = 309
    RUN_0060 = 310
    RUN_0061 = 311
    RUN_0062 = 312
    RUN_0063 = 313
    RUN_0064 = 314
    RUN_0065 = 315
    RUN_0066 = 316
    RUN_0067 = 317
    RUN_0068 = 318
    RUN_0069 = 319
    RUN_0070 = 320
    RUN_0071 = 321
    RUN_0072 = 322
    RUN_0073 = 323
    RUN_0074 = 324
    RUN_0075 = 325
    RUN_0076 = 326
    RUN_0077 = 327
    RUN_0078 = 328
    RUN_0079 = 329
    RUN_0080 = 330
    RUN_0081 = 331
    RUN_0082 = 332
    RUN_0083 = 333
    RUN_0084 = 334
    RUN_0085 = 335
    RUN_0086 = 336
    RUN_0087 = 337
    RUN_0088 = 338
    RUN_0089 = 339
    RUN_0090 = 340
    RUN_0091 = 341
    RUN_0092 = 342
    RUN_0093 = 343
    RUN_0094 = 344
    RUN_0095 = 345
    RUN_0096 = 346
    RUN_0097 = 347
    RUN_0098 = 348
    RUN_0099 = 349
    RUN_LAST = RUN_0099

    ERROR_LAST = RUN_LAST