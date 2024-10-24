import re


def get_loss(filename):

	with open(filename, "r", encoding="utf-8") as file:
		data = file.read().strip("\n").strip().split("\n")

	train_loss = list()
	validation_loss = list()

	for i, line in enumerate(data):
		print(i, line)
		if i % 2 == 0:
			search = re.search(f"'loss': ([0-9.e-]+)", line)
			train_loss.append(float('{:.5f}'.format(float(search.group(1)))))
		else:
			search = re.search(f"'eval_loss': ([0-9.e-]+)", line)
			validation_loss.append(float('{:.5f}'.format(float(search.group(1)))))

	print(f"{train_loss}\n--------------\n{validation_loss}")

	return train_loss, validation_loss


def main():
	get_loss("data/fredt5.txt")


if __name__ == "__main__":
	main()