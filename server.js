const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
app.use(bodyParser.json());
app.use(cors());

app.post("/scrape", (req, res) => {
  const { url } = req.body;
  const scriptPath = path.join(__dirname, "main.py");
  const command = `python "${scriptPath}" "${url}"`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${stderr}`);
      return res.status(500).json({ error: "Scraping failed." });
    }

    const fileName = "scraped_data.json";
    const filePath = path.join(__dirname, fileName);

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
      console.error(`Error: File ${fileName} not found.`);
      return res.status(500).json({ error: "File not found." });
    }

    // Read the content of the file
    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        console.error(`Error reading file ${fileName}: ${err}`);
        return res.status(500).json({ error: "Failed to read file." });
      }

      // Parse JSON data
      let scrapedData;
      try {
        scrapedData = JSON.parse(data);
      } catch (parseError) {
        console.error(`Error parsing JSON data: ${parseError}`);
        return res.status(500).json({ error: "Failed to parse JSON data." });
      }

      // Send the scraped data as JSON response
      res.json({ data: scrapedData });
    });
  });
});

app.use("/", (req, res) => {
  res.send("hello World");
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
