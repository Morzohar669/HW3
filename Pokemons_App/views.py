from django.shortcuts import render

# Create your views here.
import Pokemons_App.views
from Pokemons_App.models import Pokemons


def index(request):
    return render(request, 'index.html')
#sddss

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

    if request.method == 'POST' and request.POST:
        attack = request.POST["attack"]
        count = request.POST["count"]

        if int(attack) >= 0 and int(count) >= 0:
            sql3 = f"""
                SELECT DISTINCT 1 as Name, Pokemons_with_amount.Type 
                FROM (SELECT Pokemons.*, Types.type_amount
                      FROM Pokemons,
                           (SELECT Type, COUNT(*) AS type_amount
                            FROM Pokemons
                            GROUP BY Type) Types
                      WHERE Pokemons.Type = Types.Type) Pokemons_with_amount
                WHERE (Attack > {attack})
                  AND (type_amount > {count});
                      """
            sql_res3 = Pokemons.objects.raw(sql3)
            error = ''
        else:
            sql_res3 = ''
            error = """ Your input is invalid.. Please enter positive values"""

    else:
        sql_res3 = ''
        error = ''

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
                  {'error': error, 'sql_res1': sql_res1, 'sql_res2': sql_res2, 'sql_res3': sql_res3,
                   'sql_res4': sql_res4})


def add(request):
    if request.method == 'POST' and request.POST:
        name = request.POST["Name"]
        typ = request.POST["Type"]
        generation = request.POST["Generation"]
        legendary = request.POST["Legendary"]
        hp = request.POST["HP"]
        attack = request.POST["Attack"]
        defense = request.POST["Defense"]

        name_error = ""
        typ_error = ""
        gen_error = ""
        hp_error = ""
        attack_error = ""
        defense_error = ""

        if len(name) < 2 or len(name) > 50:
            name_error = "please enter a valid name (between 2-50 characters)"

        if len(typ) > 50 or len(typ) == 0:
            typ_error = "please enter a valid type (between 1-50 characters)"

        valid_gen = [1, 2, 3, 4, 5, 6]

        if (int(generation) not in valid_gen) or (((float(generation)) % 1) != 0.0):
            gen_error = "please enter a valid name (int between 1-6)"

        if int(hp) == 0 or int(hp) > 300 or (((float(hp)) % 1) != 0.0):
            hp_error = "please enter a valid hp (int between 1-300)"

        if int(attack) == 0 or int(attack) > 300 or (((float(attack)) % 1) != 0.0):
            attack_error = "please enter a valid attack (int between 1-300)"

        if int(defense) == 0 or int(defense) > 300 or (((float(defense)) % 1) != 0.0):
            defense_error = "please enter a valid defense (int between 1-300)"

        if not (
                name_error == "" or typ_error == "" or gen_error == "" or hp_error == "" or attack_error == "" or defense_error == ""):
            new_content = Pokemons(Name=name,
                                   Type=typ,
                                   Generation=generation,
                                   Legendary=legendary,
                                   HP=hp,
                                   Attack=attack,
                                   Defense=defense)
            new_content.save()
    return render(request, 'add.html',
                  {'name_error': name_error, 'typ_error': typ_error, 'gen_error': gen_error, 'hp_error': hp_error,
                   'attack_error': attack_error, 'defense_error': defense_error})
