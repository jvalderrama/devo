resource "aws_instance" "server-devo" {
  ami = "${var.ami_id}"
  instance_type = "${var.instance_type}"
}