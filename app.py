import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to load real estate dataset (Dummy example with fictional data)
def load_real_estate_data():
    data = {
        'Property Name': ['Property A', 'Property B', 'Property C', 'Property D', 'Property E', 
                          'Property F', 'Property G', 'Property H', 'Property I', 'Property J', 
                          'Property K', 'Property L', 'Property M', 'Property N', 'Property O', 
                          'Property P', 'Property Q', 'Property R', 'Property S', 'Property T'],
        'Property Price': [500000, 600000, 450000, 700000, 550000, 750000, 620000, 800000, 470000, 
                           530000, 680000, 720000, 590000, 850000, 920000, 780000, 600000, 680000, 
                           580000, 670000],
        'Property Taxes': [3000, 2500, 4000, 1800, 3500, 2000, 4200, 2300, 3200, 2600, 3800, 1800, 
                           2800, 2100, 4000, 2700, 3900, 3200, 2500, 4100],
        'Population': [5000, 7000, 3000, 10000, 8000, 6000, 8500, 11000, 4000, 4500, 7200, 9500, 
                       5000, 7800, 9000, 8500, 6200, 8800, 6700, 9000],
        'School Rating': [4.5, 3.8, 4.2, 4.9, 3.7, 4.8, 3.9, 4.7, 4.3, 4.5, 4.2, 4.9, 3.6, 4.9, 4.1, 
                          3.8, 4.4, 4.7, 3.9, 4.6],
        'Public Transportation Score': [8.1, 6.5, 7.8, 9.3, 7.0, 8.5, 6.8, 8.2, 7.5, 8.9, 6.7, 7.9, 
                                       8.2, 7.0, 8.6, 6.5, 7.9, 8.1, 7.2, 8.4]
    }

    df = pd.DataFrame(data)
    return df

# Function to calculate property score based on user preferences
def calculate_property_score(df, price_input, school_rating_input, public_transportation_input):
    df['Price_Score'] = 1 - (df['Property Price'] - price_input) / price_input
    df['School_Score'] = df['School Rating'] / school_rating_input
    df['Transportation_Score'] = df['Public Transportation Score'] / public_transportation_input

    df['Overall_Score'] = (df['Price_Score'] + df['School_Score'] + df['Transportation_Score']) / 3
    return df

# Create an animated horizontal bar graph to visualize property prices and other factors over time
def animate_property_data(filtered_df):
    # Separate plots for each factor
    fig_price, ax_price = plt.subplots(figsize=(8, 5))
    fig_taxes, ax_taxes = plt.subplots(figsize=(8, 5))
    fig_population, ax_population = plt.subplots(figsize=(8, 5))
    fig_school_rating, ax_school_rating = plt.subplots(figsize=(8, 5))
    fig_public_transport, ax_public_transport = plt.subplots(figsize=(8, 5))

    fig_price.suptitle("Property Price Over Time for Filtered Properties")
    fig_taxes.suptitle("Property Taxes Over Time for Filtered Properties")
    fig_population.suptitle("Population Over Time for Filtered Properties")
    fig_school_rating.suptitle("School Rating Over Time for Filtered Properties")
    fig_public_transport.suptitle("Public Transportation Score Over Time for Filtered Properties")

    bar_colors = ['teal', 'orange', 'green', 'blue', 'purple']
    bar_labels = ['Price', 'Taxes', 'Population', 'School Rating', 'Public Transportation']
    bar_data_columns = ['Property Price', 'Property Taxes', 'Population', 'School Rating', 'Public Transportation Score']

    bars_price = ax_price.barh(filtered_df.index, filtered_df['Property Price'], color=bar_colors[0], label=bar_labels[0])
    bars_taxes = ax_taxes.barh(filtered_df.index, filtered_df['Property Taxes'], color=bar_colors[1], label=bar_labels[1])
    bars_population = ax_population.barh(filtered_df.index, filtered_df['Population'], color=bar_colors[2], label=bar_labels[2])
    bars_school_rating = ax_school_rating.barh(filtered_df.index, filtered_df['School Rating'], color=bar_colors[3], label=bar_labels[3])
    bars_public_transport = ax_public_transport.barh(filtered_df.index, filtered_df['Public Transportation Score'], color=bar_colors[4], label=bar_labels[4])

    for ax in [ax_price, ax_taxes, ax_population, ax_school_rating, ax_public_transport]:
        ax.set_yticks(filtered_df.index)
        ax.set_yticklabels(filtered_df['Property Name'])
        ax.legend(loc='lower right')

    def update(frame):
        for i in range(len(filtered_df)):
            bars_price[i].set_width(filtered_df['Property Price'].iloc[i] * (frame + 1) / 50)
            bars_taxes[i].set_width(filtered_df['Property Taxes'].iloc[i] * (frame + 1) / 50)
            bars_population[i].set_width(filtered_df['Population'].iloc[i] * (frame + 1) / 50)
            bars_school_rating[i].set_width(filtered_df['School Rating'].iloc[i] * (frame + 1) / 50)
            bars_public_transport[i].set_width(filtered_df['Public Transportation Score'].iloc[i] * (frame + 1) / 50)

    anim_price = FuncAnimation(fig_price, update, frames=50, interval=100, repeat=False)
    anim_taxes = FuncAnimation(fig_taxes, update, frames=50, interval=100, repeat=False)
    anim_population = FuncAnimation(fig_population, update, frames=50, interval=100, repeat=False)
    anim_school_rating = FuncAnimation(fig_school_rating, update, frames=50, interval=100, repeat=False)
    anim_public_transport = FuncAnimation(fig_public_transport, update, frames=50, interval=100, repeat=False)

    return anim_price, anim_taxes, anim_population, anim_school_rating, anim_public_transport

# Create a Streamlit web application
def main():
    st.title("Real Estate Data Analysis Dashboard")
    st.write("Analyze the best properties based on various data points")

    # Load the real estate dataset
    df = load_real_estate_data()

    # Sidebar to get user input for property price, school rating, and public transportation score
    st.sidebar.title("Select Filters")
    property_price_input = st.sidebar.number_input("Enter your budget (Property Price)", min_value=0, max_value=1000000, value=500000, step=10000)
    school_rating_input = st.sidebar.number_input("Select minimum School Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
    public_transportation_input = st.sidebar.number_input("Select minimum Public Transportation Score", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

    # Filter properties based on user input
    filtered_properties = df[(df['Property Price'] <= property_price_input) & (df['School Rating'] >= school_rating_input) & (df['Public Transportation Score'] >= public_transportation_input)]

    # Display filtered properties
    st.subheader("Filtered Properties")
    st.dataframe(filtered_properties)

    # Calculate property scores
    if not filtered_properties.empty:
        df_with_scores = calculate_property_score(filtered_properties, property_price_input, school_rating_input, public_transportation_input)

        # Recommend best property
        st.subheader("Recommended Best Property")
        best_property = df_with_scores[df_with_scores['Overall_Score'] == df_with_scores['Overall_Score'].max()]
        st.dataframe(best_property)

        # Visualize property data for filtered properties using matplotlib horizontal bar graph
        st.subheader("Animated Property Data")
        anim_price, anim_taxes, anim_population, anim_school_rating, anim_public_transport = animate_property_data(filtered_properties)
        
        # Save each animation to a separate file
        anim_price_output = f"anim_price_{property_price_input:.0f}.gif"
        anim_taxes_output = f"anim_taxes_{property_price_input:.0f}.gif"
        anim_population_output = f"anim_population_{property_price_input:.0f}.gif"
        anim_school_rating_output = f"anim_school_rating_{property_price_input:.0f}.gif"
        anim_public_transport_output = f"anim_public_transport_{property_price_input:.0f}.gif"

        anim_price.save(anim_price_output, writer='pillow')
        anim_taxes.save(anim_taxes_output, writer='pillow')
        anim_population.save(anim_population_output, writer='pillow')
        anim_school_rating.save(anim_school_rating_output, writer='pillow')
        anim_public_transport.save(anim_public_transport_output, writer='pillow')

        # Display each animation separately
        st.image(anim_price_output, use_column_width=True)
        st.image(anim_taxes_output, use_column_width=True)
        st.image(anim_population_output, use_column_width=True)
        st.image(anim_school_rating_output, use_column_width=True)
        st.image(anim_public_transport_output, use_column_width=True)

if __name__ == "__main__":
    main()
