local HttpService = game:GetService("HttpService")
local TeleportService = game:GetService("TeleportService")
local Players = game:GetService("Players")
local player = Players.LocalPlayer
local placeId = game.PlaceId

local cursor = ""
local bestServer = nil

repeat
    local url = "https://games.roblox.com/v1/games/"..placeId.."/servers/Public?sortOrder=Asc&limit=100"
    if cursor ~= "" then
        url = url .. "&cursor=" .. cursor
    end

    local ok, res = pcall(game.HttpGet, game, url)
    if not ok then break end

    local ok2, data = pcall(HttpService.JSONDecode, HttpService, res)
    if not ok2 or not data or not data.data then break end

    for _, sv in pairs(data.data) do
        if sv.playing < sv.maxPlayers and sv.ping then
            if not bestServer or
               (sv.playing < bestServer.playing) or
               (sv.playing == bestServer.playing and sv.ping < bestServer.ping)
            then
                bestServer = sv
            end
        end
    end

    cursor = data.nextPageCursor or ""
    task.wait(0.2)
until cursor == ""

if bestServer then
    TeleportService:TeleportToPlaceInstance(placeId, bestServer.id, player)
end