CREATE OR REPLACE VIEW SkaterStats AS
SELECT
    GP.Player as PlayerId,
    GP.fullname AS Name,
    GP.DraftYear, 
    GP.DraftRound, 
    GP.DraftPosition,
    NVL(GP.GamesPlayed, 0) as GP,
    NVL(G.Goals, 0) as Goals,
    NVL(PA.PrimaryAssists, 0) as PAssists,
    NVL(SA.SecondaryAssists, 0) as SAssists,
    (NVL(G.Goals, 0)+ NVL(PA.PrimaryAssists, 0) + NVL(SA.SecondaryAssists, 0)) AS Points,
    ROUND(((NVL(G.Goals, 0) + NVL(PA.PrimaryAssists, 0) + NVL(SA.SecondaryAssists, 0)) / GP.GamesPlayed), 2) AS PPG,
    NVL(S.Shots, 0) AS Shots,
    NVL(C.Corsi, 0) AS MS,
    NVL(B.Blocked, 0) as Blocked,
    (NVL(S.Shots, 0) + NVL(C.Corsi, 0) + NVL(B.Blocked, 0)) AS Corsi,
    NVL((S.Shots + C.Corsi),0) AS Fenwick,
    NVL(Bs.Blocks, 0) as Blocks,
    NVL(H.Hits, 0) as Hits,
    NVL(Hs.Hit, 0) as TimesHit,
    NVL(P.Penalty, 0) as PenT,
    NVL(P2.PenaltyDrawn, 0) as PenD,
    (NVL(P2.PenaltyDrawn, 0) - NVL(P.Penalty, 0)) as PenDiff,
    NVL(FW.FOWin, 0) as FOWin,
    NVL(FL.FOLoss, 0) as FOLOSS,
    (NVL(FW.FOWin, 0) - NVL(FL.FOLoss, 0)) as FODiff
FROM 
   ( SELECT
        PlayerId as Player ,Player.FullName, Player.DraftYear, Player.DraftRound, Player.DraftPosition,
        NVL(COUNT(DISTINCT Game_GameID),0) AS GamesPlayed
    FROM
        (
            SELECT Player_1 AS PlayerId, Game_GameID FROM GameEvent
            UNION
            SELECT Player_2 AS PlayerId, Game_GameID FROM GameEvent
            UNION
            SELECT Player_3 AS PlayerId, Game_GameID FROM GameEvent
        ) CombinedPlayers
    INNER JOIN Player ON Player.Player_Id = CombinedPlayers.PlayerId
    WHERE CombinedPlayers.PlayerId IS NOT NULL
    GROUP BY CombinedPlayers.PlayerId, Player.FullName, Player.DraftYear, Player.DraftRound, Player.DraftPosition
) GP 

LEFT OUTER JOIN (
    SELECT
        Player_1 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Goals
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_1
    WHERE
        name = 'goal' and eventperiod < 5
    GROUP BY
        Player_1, Player.fullname, Player.DraftYear, Player.DraftRound, Player.DraftPosition
) G ON G.Player = GP.Player
LEFT OUTER JOIN (
    SELECT
        Player_2 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS PrimaryAssists
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_2
    WHERE
        name = 'goal' and eventperiod < 5
    GROUP BY
        Player_2, Player.fullname
) PA ON G.Player = PA.Player
LEFT OUTER JOIN (
    SELECT
        Player_3 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS SecondaryAssists
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_3
    WHERE
        name = 'goal' and eventperiod < 5
    GROUP BY 
        Player_3, Player.fullname
) SA ON G.Player = SA.Player
LEFT OUTER  JOIN (
    SELECT
        Player_1 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Shots
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_1
    WHERE
        name = 'shot-on-goal' and eventperiod < 5
    GROUP BY
        Player_1, Player.fullname
) S ON G.Player = S.Player
LEFT OUTER  JOIN (
    SELECT
        Player_1 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Corsi
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_1
    WHERE
        name = 'missed-shot' and eventperiod < 5
    GROUP BY
        Player_1, Player.fullname
) C ON G.Player = C.Player
LEFT OUTER JOIN (
    SELECT
        Player_2 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Blocked
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_2
    WHERE
        name = 'blocked-shot' and eventperiod < 5
    GROUP BY
        Player_2, Player.fullname
) B ON G.Player = B.Player
LEFT OUTER JOIN (
    SELECT
        Player_1 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Blocks
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_1
    WHERE
        name = 'blocked-shot' and eventperiod < 5
    GROUP BY
        Player_1, Player.fullname
) Bs ON G.Player = Bs.Player
LEFT OUTER JOIN (
    SELECT
        Player_1 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Hits
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_1
    WHERE
        name = 'hit' and eventperiod < 5
    GROUP BY
        Player_1, Player.fullname
) H ON G.Player = H.Player
LEFT OUTER JOIN (
    SELECT
        Player_2 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Hit
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_2
    WHERE
        name = 'hit' and eventperiod < 5
    GROUP BY
        Player_2, Player.fullname
) Hs ON G.Player = Hs.Player
LEFT OUTER  JOIN (
    SELECT
        Player_1 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS Penalty
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_1
    WHERE
        name = 'penalty' and eventperiod < 5
    GROUP BY
        Player_1, Player.fullname
) P ON G.Player = P.Player
LEFT OUTER  JOIN (
    SELECT
        Player_2 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS PenaltyDrawn
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_2
    WHERE
        name = 'penalty' and eventperiod < 5
    GROUP BY
        Player_2, Player.fullname
) P2 ON G.Player = P2.Player
LEFT OUTER  JOIN (
    SELECT
        Player_1 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS FOWin
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_1
    WHERE
        name = 'faceoff' and eventperiod < 5
    GROUP BY
        Player_1, Player.fullname
) FW ON G.Player = FW.Player
LEFT OUTER JOIN (
    SELECT
        Player_2 AS Player,
        Player.fullname,
        NVL(COUNT(playid), 0) AS FOLoss
    FROM
        GameEvent
        INNER JOIN Player ON Player.Player_Id = GameEvent.Player_2
    WHERE
        name = 'faceoff' and eventperiod < 5
    GROUP BY
        Player_2, Player.fullname
) FL ON G.Player = FL.Player;