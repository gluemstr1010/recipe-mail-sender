from smtp import send_mail
from recept import Recept
from req import *

smtp_server = "smtp.gmail.com"
port = 587

sender = "XXXXXX@gmail.com"
recipient = "XXXXXXX@gmail.com"
recipients = [recipient]

subject = "Automated recipe notification"

# Crafting mail
def create_message(recept: Recept):
    msg_start = f"""Get ready to cook the {recept.meal_Name}!
Category: {recept.meal_Category}
Geography: {recept.meal_Geography} \n\n"""

    msg_end = f"""\n\n{recept.meal_Image}
Video:
{recept.meal_Video}
Source: {recept.meal_source}  """

    ingr_str = f"""Recipe Ingredients:"""
    for i in range(1,len(recept.meal_Ingredients)):
        ingredient = recept.meal_Ingredients[i]
        measure = recept.meal_Measures[i]

        ingr_instr = ingredient + ": " + measure

        ingr_str += f"\n{ingr_instr}"

    instructions = f"""\n\nRecipe Instructions:
{recept.meal_Instructions}"""
    
    msg_start += ingr_str
    msg_start += instructions
    msg_start += msg_end

    return msg_start

def main():
    actual_res_content = contact_api() ## contacting api, getting api content
    
    rcpt = Recept(actual_res_content["strMeal"],actual_res_content["strCategory"],actual_res_content["strArea"],actual_res_content["strInstructions"],
     actual_res_content["strMealThumb"],actual_res_content["strYoutube"],get_list(actual_res_content,"Ingredient"),get_list(actual_res_content,"Measure"),actual_res_content["strSource"])

    message = create_message(rcpt)

    send_mail(smtp_server,port,subject,message,sender,recipients)

if __name__ == '__main__':
    main()