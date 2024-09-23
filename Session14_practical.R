# A Shiny app showing penguin bill size relationships
# Jeff Oliver
# jcoliver@arizona.edu
# 2021-07-30

library(shiny)
library(palmerpenguins)
library(ggplot2)

# Define UI for application that draws a scatterplot
ui <- fluidPage(
  
  # Application title
  titlePanel("Penguin size relationships"),
  
  # Sidebar with text input for penguin species
  sidebarLayout(
    sidebarPanel(
      selectInput(inputId = "species",
                  label = "Species",
                  choices = unique(penguins$species))
    ),
    
    # Show plot and statistical results
    mainPanel(
      plotOutput("distPlot"),
      tableOutput("statsTable")
    )
  )
)

# Define server logic required to draw a scatterplot
server <- function(input, output) {
  
  # Make plot of bill depth vs. bill length
  output$distPlot <- renderPlot({
    ggplot(data = penguins[penguins$species == input$species, ], 
           mapping = aes(x = bill_length_mm, 
                         y = bill_depth_mm,
                         color = sex)) +
      geom_point() +
      xlab("Bill length (mm)") +
      ylab("Bill depth (mm)")
  })
  
  # Add results of a linear model to output
  output$statsTable <- renderTable({
    # Create the linear model
    model <- lm(formula = bill_depth_mm ~ bill_length_mm,
                data = penguins[penguins$species == input$species, ])
    # Extract summary statistics
    model_summary <- summary(model)
    # Print coefficient table
    model_summary$coefficients
  }, rownames = TRUE)
}

# Run the application 
shinyApp(ui = ui, server = server)
