# Labeling Guidelines: EN NLI

Завдання полягає у класифікації логічного зв'язку між двома реченнями: Передумовою (Premise) та Гіпотезою (Hypothesis).

## Клас 1: Entailment (Логічне слідування)
**Визначення**: Гіпотеза є абсолютно правдивою, виходячи виключно з інформації, наданої в Передумові. Якщо Передумова істинна, Гіпотеза не може бути хибною.
* *Приклад 1 (Входить)*: 
  * Premise: A soccer game with multiple males playing. 
  * Hypothesis: Some men are playing a sport.
* *Приклад 2 (Входить)*: 
  * Premise: Two dogs are running through a field.
  * Hypothesis: There are animals outdoors.
* *Приклад 3 (Не входить)*: 
  * Premise: A boy plays with a ball. 
  * Hypothesis: The boy is happy. *(Ми не знаємо його емоцій з передумови, це Neutral).*

## Клас 2: Contradiction (Суперечність)
**Визначення**: Гіпотеза є абсолютно хибною, якщо Передумова є правдивою. Ці дві події/ситуації не можуть відбуватися одночасно.
* *Приклад 1 (Входить)*: 
  * Premise: A man inspects the uniform of a figure in some East Asian country.
  * Hypothesis: The man is sleeping.
* *Приклад 2 (Входить)*: 
  * Premise: A black race car starts up in front of a crowd of people.
  * Hypothesis: A man is driving down a lonely road.
* *Приклад 3 (Не входить)*: 
  * Premise: A man is riding a bicycle. 
  * Hypothesis: A woman is riding a bicycle. *(Це суперечність, тільки якщо йдеться про одну й ту саму людину, але за правилами SNLI зміна статі головного актора є суперечністю).*

## Клас 3: Neutral (Нейтральність)
**Визначення**: Гіпотеза може бути як правдивою, так і хибною; інформації в Передумові недостатньо для точного висновку. Гіпотеза часто додає нові деталі, які не суперечать передумові, але й не випливають з неї.
* *Приклад 1 (Входить)*: 
  * Premise: An older and younger man smiling.
  * Hypothesis: Two men are smiling and joking at the cats playing on the floor.
* *Приклад 2 (Входить)*: 
  * Premise: A woman selling food on the street.
  * Hypothesis: The woman is selling hot dogs.
* *Приклад 3 (Не входить)*: 
  * Premise: A kid jumping on a trampoline. 
  * Hypothesis: A kid is jumping. *(Це Entailment, а не Neutral, бо стрибання є прямим фактом).*