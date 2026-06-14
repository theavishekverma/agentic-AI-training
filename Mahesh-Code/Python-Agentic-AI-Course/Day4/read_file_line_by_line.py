#read file line by line

#open file syntax
file_obj=open("stock.csv","r")

#read file line by line
for line in file_obj:
    if line.startswith("stock_name"):
        continue
    # calculate the price change
    data = line.split(",")    
    #reove leading and trailing whitespace characters and newline characters
    data = [x.strip() for x in data]
    # calculate stock up or down
    price_change = int(data[2]) - int(data[1])
    if price_change > 0:
        data.append("up")
    elif price_change < 0:
        data.append("down")
    else:
        data.append("no change")

    #print the stock name and price change and store into file
    file_o = open("stock_price_change.txt", "a")
    file_o.write(f"{data[0]}: {data[4]}\n")           
    file_o.close()

file_obj.close()