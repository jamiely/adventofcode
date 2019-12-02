namespace AoC2019

module Say =
    let hello name =
        printfn "Hello %s" name

module Day1 =
    let fuelRequiredForMass mass =
        int(floor(float(mass) / 3.0)) - 2

    let rec fuelRequiredForMassRecurse mass =
        if mass <= 0 then 0
        else
            let fuel = fuelRequiredForMass mass
            if fuel <= 0 then 0
            else fuel + (fuelRequiredForMassRecurse fuel)
    
    let fuelRequiredCombined mass =
        let fuel = fuelRequiredForMass mass
        fuel + (fuelRequiredForMassRecurse fuel)
    
    let run filepath =
        let lines = System.IO.File.ReadLines(filepath)
        let fuels = lines |> Seq.map(int >> fuelRequiredCombined)
        Seq.sum(fuels)
