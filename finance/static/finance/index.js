const margin = { top: 20, right: 20, bottom: 30, left: 50 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const x = d3.scaleTime().range([0, width]);
    const y = d3.scaleLinear().range([height, 0]);


    $(document).ready(function () {
      $('tbody').on('click', 'th', function () {
        const stock_symbol = $(this).text();
        const stock_index = $(this).attr("id");
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
          type: 'POST',
          url: 'stock_data/get/',
          data: {
            'stock_symbol': stock_symbol,
            'stock_index': stock_index,
            csrfmiddlewaretoken: csrftoken
          },
          success: function (stock_data) {

            stock_data.forEach(function (d) {
              d.date = new Date(d.date);
              d.close = d.close;
            });

            d3.select("#line-chart").selectAll("*").remove();

            const line = d3.line()
              .x(function (d) { return x(d.date); })
              .y(function (d) { return y(d.close); });

            const svg = d3.select("#line-chart")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
              .append("g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            const xAxis = d3.axisBottom(x);
            const yAxis = d3.axisLeft(y);

            x.domain(d3.extent(stock_data, function (d) { return d.date; }));


            // Calculate the maximum value in the dataset
            const maxClose = d3.max(stock_data, function (d) { return d.close; });

            // Calculate the padding
            const padding = (maxClose - d3.min(stock_data, function (d) { return d.close; })) / 4;

            // Set the y domain with padding
            y.domain([d3.min(stock_data, function (d) { return d.close; }) - padding, maxClose + padding]);

            svg.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);

            svg.append("g")
              .call(yAxis);

            svg.append("path")
              .datum(stock_data)
              .attr("fill", "none")
              .attr("stroke", "steelblue")
              .attr("stroke-linejoin", "round")
              .attr("stroke-linecap", "round")
              .attr("stroke-width", 1.5)
              .attr("d", line);

            //50 day moving average line
            const ma_50 = cal_moving_average(stock_data);
            svg.append("path")
              .datum(ma_50)
              .attr("fill", "none")
              .attr("stroke", "orange")  // You can choose any color for the line
              .attr("stroke-width", 1.5)
              .attr("d", line);

            // 20 day moving average
            const ma_20 = cal_moving_average(stock_data, period = 20);
            svg.append("path")
              .datum(ma_20)
              .attr("fill", "none")
              .attr("stroke", "black")  // You can choose any color for the line
              .attr("stroke-width", 1.5)
              .attr("d", line);

            // legends
            // Create a legend
            const legend = svg.append("g")
              .attr("class", "legend")
              .attr("transform", "translate(" + (width - 100) + ", 20)");

            // Add legend for the stock line
            legend.append("rect")
              .attr("x", 0)
              .attr("y", 0)
              .attr("width", 10)
              .attr("height", 10)
              .style("fill", "steelblue");
            legend.append("text")
              .attr("x", 15)
              .attr("y", 5)
              .attr("dy", ".20em")
              .style("text-anchor", "start")
              .text("Stock Close");

            // Add legend for the moving average line
            legend.append("rect")
              .attr("x", 0)
              .attr("y", 20)
              .attr("width", 10)
              .attr("height", 10)
              .style("fill", "orange");
            legend.append("text")
              .attr("x", 15)
              .attr("y", 25)
              .attr("dy", ".20em")
              .style("text-anchor", "start")
              .text("50-DMA");

            legend.append("rect")
              .attr("x", 0)
              .attr("y", 40)
              .attr("width", 10)
              .attr("height", 10)
              .style("fill", "black");
            legend.append("text")
              .attr("x", 15)
              .attr("y", 45)
              .attr("dy", ".20em")
              .style("text-anchor", "start")
              .text("20-DMA");
          },
          error: function (error) {
            console.error(error);
          }
        });
      });
    });


    // moving average function
    const cal_moving_average = (stock_data, period = 50) => {
      const movingAveragePeriod = period;
      const movingAverage = [];
      for (let i = movingAveragePeriod - 1; i < stock_data.length; i++) {
        let sum = 0;
        for (let j = 0; j < movingAveragePeriod; j++) {
          sum += stock_data[i - j].close;
        }
        movingAverage.push({ date: stock_data[i].date, close: sum / movingAveragePeriod });
      }
      return movingAverage;
    }


    $('#update_records').on('click', function () {
        $("#update_cell").text("Updating the records...");
        $.ajax({
          type: 'GET',
          url: "{% url 'update_records' %}",
          success: function (response) {
            console.log(response)
            $("#update_cell").text("Last updated : "+response.last_updated);
           },
          error: {}
        })
      });