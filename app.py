# importing host library
import streamlit as manav

# summary package for project



# web scrapping packages for the project 




def  main():
    # summary and entity checker

    manav.title("Summarizer and Entity Checker")
    activities = ["Summarize", "Entity Checker","NER for URL"]
    choice = manav.selectbox("Select Activity",activities)
    
    if choice == "Summarizer":
        manav.subheader("Summary")
        raw_text = manav.textbox("Enter the paragraph here...")
        if manav.button('Summarize'):
            manav.write(raw_text)
    



if __name__ == "__main__":
    main()