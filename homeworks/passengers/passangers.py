# -*- encoding: utf-8 -*-


def process(data, events, car):

    for event in events:
        eType = event['type']
        if eType == "walk":
            indexes = findPassanger(data, event['passenger'])
            if indexes != -1:
                trainIndex = indexes[0]
                carIndex = indexes[1]
                personIndex = indexes[2]
                if carIndex + event['distance'] < 0 or carIndex + 1 + event['distance'] > len(data[trainIndex]['cars']):
                    return -1
                else:
                    newCarInd = carIndex + event['distance']
                    data[trainIndex]['cars'][newCarInd]['people'].append(data[trainIndex]['cars'][carIndex]['people'][personIndex])
                    del data[trainIndex]['cars'][carIndex]['people'][personIndex]
        elif eType == "switch":
            trainFrom = findTrain(data, event['train_from'])
            trainTo = findTrain(data, event['train_to'])
            if trainFrom == -1 or trainTo == -1:
                return -1
            else:
                carsToSwitch = event['cars']
                if len(data[trainFrom]['cars']) >= carsToSwitch:
                    while carsToSwitch > 0:
                        data[trainTo]['cars'].append(data[trainFrom]['cars'][-1*carsToSwitch])
                        del data[trainFrom]['cars'][-1 * carsToSwitch]
                        carsToSwitch = carsToSwitch - 1
                else:
                    return -1
        else:
            return -1
    # find and return output
    for train in data:
        for carf in train['cars']:
            if carf['name'] == car:
                return len(carf['people'])

    return -1

def findPassanger(data, givenPassanger): # array of inedexs of train, car, passanger
    for train in data:
        for car in train['cars']:
            for passanger in car['people']:
                if passanger == givenPassanger:
                    return [data.index(train), train['cars'].index(car), car['people'].index(passanger)]
    return -1

def findTrain(data, trainName):
    for train in data:
        if train['name'] == trainName:
            return data.index(train)
    return -1

