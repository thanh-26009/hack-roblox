getgenv().Config = {
    ["Team"] = "Pirates",
    ["Safe Health"] = { 40, 50 }, ---health dodge run,health back %
    ["Skip"] = {
        ["Fruit"] = {
            ["Enabled"] = true,
            ["Avoid Fruit"] = { "Portal", "Kitsune", "Tiger", "Dragon" }
        },
        ["Avoid V4"] = true
    },
    ["Hunt Method"] = {
        ["Use Move Predict"] = true,
        ["Hit and Run"] = true
    },
    ["Spam All Skill On V4"] = {
        ["Enabled"] = true,
        ["Weapons"] = { "Melee", "Gun", "Sword", "Blox Fruit" }
    },
    ["Chat"] = {
        ["Enabled"] = false,
        ["Message"] = { "ez", "bounty pls", "teddy hub" }
    },
    ["Custom Y Run"] = {
        ["Enabled"] = true,
        ["Y Run"] = 500
    },
    ["Misc"] = {
        ["Turn On V3"] = true,
        ["Turn On V4"] = true,
        ["Delete Map"] = false,
        ["FPS BOOST"] = true,
        ["White Screen"] = false,
        ["Click Delay"] = 0.5,
        ["Spin Bot"] = {
            ["Enable"] = true,
            ["Spin Speed"] = 15,
            ["Spin Radius"] = 10,
        }
        
    },
    ["Items"] = {
        ["Use"] = { "Melee", "Gun", "Sword", "Blox Fruit" },
        ["Melee"] = {
            ["Enable"] = true,
            ["Skills"] = {
                ["Z"] = { ["Enable"] = true, ["HoldTime"] = 0.6 },
                ["X"] = { ["Enable"] = true, ["HoldTime"] = 0.3 },
                ["C"] = { ["Enable"] = true, ["HoldTime"] = 0.5 }
            }
        },
        ["Blox Fruit"] = {
            ["Enable"] = true,
            ["Skills"] = {
                ["Z"] = { ["Enable"] = true, ["HoldTime"] = 0 },
                ["X"] = { ["Enable"] = true, ["HoldTime"] = 0 },
                ["C"] = { ["Enable"] = true, ["HoldTime"] = 0 },
                ["V"] = { ["Enable"] = true, ["HoldTime"] = 0 },
                ["F"] = { ["Enable"] = true, ["HoldTime"] = 0 }
            }
        },
        ["Sword"] = {
            ["Enable"] = true,
            ["Skills"] = {
                ["Z"] = { ["Enable"] = true, ["HoldTime"] = 0.8 },
                ["X"] = { ["Enable"] = true, ["HoldTime"] = 0.5 }
            }
        },
        ["Gun"] = {
            ["Enable"] = true,
            ["Skills"] = {
                ["Z"] = { ["Enable"] = true, ["HoldTime"] = 0 },
                ["X"] = { ["Enable"] = true, ["HoldTime"] = 0 }
            }
        }
    },
    ["Webhook"] = {
        ["Enabled"] = true, 
        ["Url"] = "https://discord.com/api/webhooks/1443617207765700701/_3n2NIaDoplc6SPuDumk88xUFcWdDcUtxB9JoT8lDhUJgNKu4YPoZUqmINj_iQuzm2jH"---input webhook 
    }
}
loadstring(game:HttpGet("https://raw.githubusercontent.com/Teddyseetink/Haidepzai/refs/heads/main/TeddyHub-BountyEzz.lua"))()
