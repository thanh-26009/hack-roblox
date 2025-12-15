_G.MeeTsuoAutoBountySettings = {
    Set = {
        Team = "Pirates" -- Marines
    },

    Chat = {
        Enabled = false, -- Yes --&gt; true, No --&gt; false.
        List = {""}
    },

    Melee = {
        Enable = true, 
        Z = {Enable = true, HoldTime = 0.1}, -- HoldTime --&gt; 0.1second can KeyPressHold/TapHold
        X = {Enable = true, HoldTime = 0.1},
        C = {Enable = true, HoldTime = 0.1},
        Delay = 1.5 -- Weapons Switch Delay
    },

    Sword = {
        Enable = true,
        Z = {Enable = true, HoldTime = 0.1},
        X = {Enable = true, HoldTime = 0.1},
        Delay = 1
    },

    Gun = {
        Enable = true,
        Z = {Enable = true, HoldTime = 0.1},
        X = {Enable = true, HoldTime = 0.1},
        Delay = 1,
        GunMode = false
    },

    Fruit = {
        Enable = true,
        Z = {Enable = true, HoldTime = 0.1},
        X = {Enable = true, HoldTime = 0.1},
        C = {Enable = true, HoldTime = 0.1},
        V = {Enable = true, HoldTime = 0.1}, -- false If V Skill Is Transform Fruits
        F = {Enable = true, HoldTime = 0.1},
        Delay = 1
    },

    Click = {
        FastAttack = true, -- Fast Attack
        AutoClick = true -- Auto Click
    },

    Hunt = {
        Min = 0, -- only hunt on target that in between 0 to 30m target
        Max = 30000000 -- you can adjust these
    },

    Skip = {
        V4 = true, -- Skip If Target In V4 Transform
        Fruit = false,
        FruitList = {"Buddha", "Leopard", "T-Rex"},
        MinLevel = 450 -- Skip If Target below 450 level below from your level
    }, -- example my level 2800 - 450 = 2350 can hunt if target level below then skip

    SafeHealth = {
        Health = 4000 -- For escape from opponent 
    },

    Another = {
        V3 = true,
        V4 = true,
        CustomHealth = true,
        Health = 12000, -- V3 Work At This Health HP
        WhiteScreen = false,
        FPSBoots = true,
        CamLock = true
    }
}

loadstring(game:HttpGet("https://api.junkie-development.de/api/v1/luascripts/public/f464acf4b17cbd0d6f09cf21ed4d3bbf010c4d98b5a3e3ed7a7531eb1b3248d2/download"))()