const { randomUUID } = require("crypto");

// Demo Companies
const companies = [
  {
    name: "EcoGrid Solutions",
    location: "Amsterdam",
    statuses: [
      {
        commodity: "Electricity",
        status: "surplus",
        amount: { value: 500, measurement_unit: "MWh" },
      },
      {
        commodity: "Heat",
        status: "deficit",
        amount: { value: 200, measurement_unit: "GJ" },
      },
    ],
  },
  {
    name: "GreenHydro Corp",
    location: "Berlin",
    statuses: [
      {
        commodity: "Hydrogen",
        status: "surplus",
        amount: { value: 300, measurement_unit: "kg" },
      },
      {
        commodity: "Electricity",
        status: "deficit",
        amount: { value: 400, measurement_unit: "MWh" },
      },
    ],
  },
  {
    name: "SolarTech Industries",
    location: "Barcelona",
    statuses: [
      {
        commodity: "Electricity",
        status: "surplus",
        amount: { value: 800, measurement_unit: "MWh" },
      },
      {
        commodity: "Gas",
        status: "deficit",
        amount: { value: 150, measurement_unit: "MMBtu" },
      },
    ],
  },
  {
    name: "WindPower Dynamics",
    location: "Copenhagen",
    statuses: [
      {
        commodity: "Electricity",
        status: "surplus",
        amount: { value: 600, measurement_unit: "MWh" },
      },
      {
        commodity: "Heat",
        status: "surplus",
        amount: { value: 250, measurement_unit: "GJ" },
      },
    ],
  },
  {
    name: "ThermalEnergy Plus",
    location: "Vienna",
    statuses: [
      {
        commodity: "Heat",
        status: "surplus",
        amount: { value: 450, measurement_unit: "GJ" },
      },
      {
        commodity: "Gas",
        status: "surplus",
        amount: { value: 200, measurement_unit: "MMBtu" },
      },
    ],
  },
  {
    name: "HydrogenTech Solutions",
    location: "Stockholm",
    statuses: [
      {
        commodity: "Hydrogen",
        status: "surplus",
        amount: { value: 500, measurement_unit: "kg" },
      },
      {
        commodity: "Electricity",
        status: "deficit",
        amount: { value: 300, measurement_unit: "MWh" },
      },
    ],
  },
];

// Commodity configurations
const commodityConfigs = {
  Electricity: {
    basePrice: 80,
    unit: "MWh",
    volatility: 0.15,
    seasonalImpact: 0.2,
  },
  Hydrogen: {
    basePrice: 10,
    unit: "kg",
    volatility: 0.25,
    seasonalImpact: 0.1,
  },
  Heat: {
    basePrice: 30,
    unit: "GJ",
    volatility: 0.1,
    seasonalImpact: 0.3,
  },
  Gas: {
    basePrice: 20,
    unit: "MMBtu",
    volatility: 0.2,
    seasonalImpact: 0.25,
  },
};

// Generate random price with seasonal variation
function generatePrice(commodity, date) {
  const config = commodityConfigs[commodity];
  const seasonalFactor =
    Math.sin(((date.getMonth() + 1) * Math.PI) / 6) * config.seasonalImpact;
  const randomFactor = (Math.random() - 0.5) * 2 * config.volatility;
  return config.basePrice * (1 + seasonalFactor + randomFactor);
}

// Generate random amount for a commodity
function generateAmount(commodity) {
  const config = commodityConfigs[commodity];
  const baseAmount = Math.floor(Math.random() * 100) + 50;
  return {
    value: baseAmount,
    measurement_unit: config.unit,
  };
}

// Generate trades for the past year
function generateHistoricalTrades() {
  const trades = [];
  const endDate = new Date();
  const startDate = new Date(endDate);
  startDate.setFullYear(startDate.getFullYear() - 1);

  // Generate multiple trades per day
  for (
    let date = startDate;
    date <= endDate;
    date.setHours(date.getHours() + 4)
  ) {
    const numTrades = Math.floor(Math.random() * 3) + 1;

    for (let i = 0; i < numTrades; i++) {
      const commodity =
        Object.keys(commodityConfigs)[
          Math.floor(Math.random() * Object.keys(commodityConfigs).length)
        ];
      const requesterIdx = Math.floor(Math.random() * companies.length);
      let fulfillerIdx;
      do {
        fulfillerIdx = Math.floor(Math.random() * companies.length);
      } while (fulfillerIdx === requesterIdx);

      const price = generatePrice(commodity, date);
      const amount = generateAmount(commodity);

      trades.push({
        id: randomUUID(),
        commodity,
        type: Math.random() < 0.5 ? "buy" : "sell",
        amount,
        price: {
          value: price,
          currency: "EUR",
        },
        status: "Completed",
        time: new Date(date),
        requester_company: companies[requesterIdx].name,
        fulfiller_company: companies[fulfillerIdx].name,
      });
    }
  }

  return trades;
}

// Generate the data
const historicalTrades = generateHistoricalTrades();

// Write to files
const fs = require("fs");

// Save companies
fs.writeFileSync("demo_companies.json", JSON.stringify(companies, null, 2));

// Save historical trades
fs.writeFileSync("demo_trades.json", JSON.stringify(historicalTrades, null, 2));

console.log(`Generated ${companies.length} companies`);
console.log(`Generated ${historicalTrades.length} historical trades`);
