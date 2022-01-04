from django.shortcuts import render

# Create your views here.
from Pokemons_App.models import Pokemons


def index(request):
    return render(request, 'index.html')


def query(request):
    sql1 = """
    SELECT Pokemons.Generation, Pokemons.Name
    FROM
         Pokemons
         ,
        (SELECT Generation, MAX(hp + Defense + Attack) as total
        FROM Pokemons
        group by Generation) Totals
    
    WHERE (Pokemons.Generation = Totals.Generation) AND
          (Legendary = 'true') AND (HP + Attack + Defense = total)
    order by Pokemons.Generation asc
          """
    sql_res1 = Pokemons.objects.raw(sql1)

    sql2 = """
    SELECT Pokemons.Type ,Pokemons.Name
    FROM Pokemons
    
    EXCEPT
    
    SELECT DISTINCT P2.type ,P2.name
    FROM Pokemons P1,
         Pokemons P2
    
    WHERE ((P1.Type = P2.Type) AND (P1.Name <> P2.Name))
      AND ((P1.HP >= P2.HP) OR (P1.Defense >= P2.Defense) OR (P1.Attack >= P2.Attack));
              """
    sql_res2 = Pokemons.objects.raw(sql2)

    sql3 = """
        SELECT DISTINCT 1 as Name, Pokemons_with_amount.Type 
        FROM (SELECT Pokemons.*, Types.type_amount
              FROM Pokemons,
                   (SELECT Type, COUNT(*) AS type_amount
                    FROM Pokemons
                    GROUP BY Type) Types
              WHERE Pokemons.Type = Types.Type) Pokemons_with_amount
        WHERE (Attack > 150)
          AND (type_amount > 80);
              """
    sql_res3 = Pokemons.objects.raw(sql3)

    sql4 = """
        SELECT 1 as Name, Diff_SUM.Type, FORMAT(ROUND(((Sum_Of_Diffs * 1.0) / type_amount),2),'N2') AS max_average_instability
        FROM (SELECT Type, SUM(Diff) as Sum_Of_Diffs
              FROM (SELECT Pokemons.*, ABS(Pokemons.Attack - Pokemons.Defense) AS Diff
                    FROM Pokemons) Pokemons_with_diff
              GROUP BY Type) Diff_SUM
             ,
             (SELECT Type, COUNT(*) AS type_amount
              FROM Pokemons
              GROUP BY Type) Types
        WHERE Diff_SUM.Type = Types.Type
        
        EXCEPT
        
        SELECT 1 as Name, All_Instability1.Type , FORMAT(ROUND(All_Instability1.average_instability, 2),'N2') as max_average_instability
        FROM (SELECT Diff_SUM.Type, ((Sum_Of_Diffs * 1.0) / type_amount) AS average_instability
                FROM (SELECT Type, SUM(Diff) as Sum_Of_Diffs
                      FROM (SELECT Pokemons.*, ABS(Pokemons.Attack - Pokemons.Defense) AS Diff
                            FROM Pokemons) Pokemons_with_diff
                      GROUP BY Type) Diff_SUM
                     ,
                     (SELECT Type, COUNT(*) AS type_amount
                      FROM Pokemons
                      GROUP BY Type) Types
                WHERE Diff_SUM.Type = Types.Type) All_Instability1
                ,
                (SELECT Diff_SUM.Type, ((Sum_Of_Diffs * 1.0) / type_amount) AS average_instability
                FROM (SELECT Type, SUM(Diff) as Sum_Of_Diffs
                      FROM (SELECT Pokemons.*, ABS(Pokemons.Attack - Pokemons.Defense) AS Diff
                            FROM Pokemons) Pokemons_with_diff
                      GROUP BY Type) Diff_SUM
                     ,
                     (SELECT Type, COUNT(*) AS type_amount
                      FROM Pokemons
                      GROUP BY Type) Types
                WHERE Diff_SUM.Type = Types.Type) All_Instability2
        WHERE All_Instability1.average_instability < All_Instability2.average_instability
              """
    sql_res4 = Pokemons.objects.raw(sql4)

    return render(request, 'Query.html',
                  {'sql_res1': sql_res1, 'sql_res2': sql_res2, 'sql_res3': sql_res3, 'sql_res4': sql_res4})


def add(request):
    return render(request, 'Add.html')