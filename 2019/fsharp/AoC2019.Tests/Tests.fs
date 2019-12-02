module AoC2019.Tests

open System
open Xunit

[<Fact>]
let ``Fuel for mass 1`` () = 
    Assert.Equal(Day1.fuelRequiredForMass(1969), 654) 

[<Fact>]
let ``Fuel for mass 2`` () = 
    Assert.Equal(Day1.fuelRequiredForMass(100756), 33583)

[<Fact>]
let ``Fuel for mass recursive 1`` () =
    Assert.Equal(Day1.fuelRequiredForMassRecurse(1969), 966)

[<Fact>]
let ``Fuel for mass recursive 2`` () =
    Assert.Equal(Day1.fuelRequiredForMassRecurse(100756), 50346)

[<Fact>]
let ``Fuel total`` () =
    Assert.Equal(Day1.run("../../../../../1.input"), 4972784)