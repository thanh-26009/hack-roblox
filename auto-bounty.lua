_G.config = {
    team = "Pirates", --? Pirates Marines
    servertohop = "Singapore",
    timetoskip = 80,
    timetohop = 600,
    autouselowgraphic = true,
    autoQ = false,
    random = false, --! random = false if u want to use custom
    autoken = true,
    enablev4 = true,
    enablev3 = true,
    blackscreen = false,
    ignorefruits = {"Portal-Portal"--[[, "Buddha-Buddha", "Dragon-Dragon", "Kitsune-Kitsune", "Leopard-Leopard"]]},
    safezone = {
        HighestHealth = 65, -- % health
        LowestHealth = 35, -- % health
    },
    methodclicks = {
        LowerHealthToM1 = 4000,
        Delay = 0.25,
        Melee = true,
        Sword = true,
        Gun = false,
    },
    custom = {
        Melee = {
            Enable = true,
            Skills = {
                Z = {
                    Enable = true,
                    Number = 3,
                    HoldTime = 0.15151515,
                },
                X = {
                    Enable = true,
                    Number = 5,
                    HoldTime = 0.15151515,
                },
                C = {
                    Enable = true,
                    Number = 4,
                    HoldTime = 0.15151515,
                },
            },
        },
        Sword = {
            Enable = true,
            Skills = {
                Z = {
                    Enable = true,
                    Number = 1,
                    HoldTime = 0.15151515,
                },
                X = {
                    Enable = true,
                    Number = 2,
                    HoldTime = 0.15151515,
                },
            },
        },
        ['Blox Fruit'] = {
            Enable = true,
            Skills = {
                Z = {
                    Enable = true,
                    Number = 4,
                    0.15151515,
                },
                X = {
                    Enable = true,
                    Number = 1,
                    HoldTime = 0.15151515,
                },
                C = {
                    Enable = true,
                    Number = 4.5,
                    HoldTime = 0.15151515,
                },
                V = {
                    Enable = true,
                    Number = 7,
                    HoldTime = 0.15151515,
                },
                F = {
                    Enable = true,
                    Number = 8,
                    HoldTime = 0.15151515,
                },
            },
        },
        Gun = {
            Enable = true,
            Skills = {
                Z = {
                    Enable = true,
                    Number = 5,
                    HoldTime = 0.15151515,
                },
                X = {
                    Enable = true,
                    Number = 1,
                    HoldTime = 0.15151515,
                },
            },
        },
    },
    webhook = {
        Enabled = true,
        Url = "https://discord.com/api/webhooks/1443617207765700701/_3n2NIaDoplc6SPuDumk88xUFcWdDcUtxB9JoT8lDhUJgNKu4YPoZUqmINj_iQuzm2jH",
    }
}

loadstring(game:HttpGet("https://raw.githubusercontent.com/RedGamer12/VisionX/refs/heads/main/bounty-obfuscated.lua"))()
