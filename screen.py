from enum import Enum, auto

class ScreenID(Enum):
    Unknown = -1
    Standby = auto()
    InsertCashOrCard = auto()
    WaitForApproval = auto()
    CashOrCardApproval = auto()
    InsertItemToWash = auto()
    WashCycle = auto()
    DryCycle = auto()
    CycleComplete = auto()
    ServiceMode = auto()
    ErrorScreen = auto()
    SelectItemToWash = auto()
    InsertEyewearToWash = auto()
    InsertJewelryToWash = auto()
    InsertPhoneToWash = auto()



# public enum ScreenID
# 	{
# 		// Token: 0x0400006B RID: 107
# 		Unknown = -1,
# 		// Token: 0x0400006C RID: 108
# 		Standby,
# 		// Token: 0x0400006D RID: 109
# 		InsertCashOrCard,
# 		// Token: 0x0400006E RID: 110
# 		WaitForApproval,
# 		// Token: 0x0400006F RID: 111
# 		CashOrCardApproval,
# 		// Token: 0x04000070 RID: 112
# 		InsertItemToWash,
# 		// Token: 0x04000071 RID: 113
# 		WashCycle,
# 		// Token: 0x04000072 RID: 114
# 		DryCycle,
# 		// Token: 0x04000073 RID: 115
# 		CycleComplete,
# 		// Token: 0x04000074 RID: 116
# 		ServiceMode,
# 		// Token: 0x04000075 RID: 117
# 		ErrorScreen,
# 		// Token: 0x04000076 RID: 118
# 		SelectItemToWash,
# 		// Token: 0x04000077 RID: 119
# 		InsertEyewearToWash,
# 		// Token: 0x04000078 RID: 120
# 		InsertJewelryToWash,
# 		// Token: 0x04000079 RID: 121
# 		InsertPhoneToWash

