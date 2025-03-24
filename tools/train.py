import argparse
from datetime import datetime
from ultralytics import YOLO

def make_parser():
    parser = argparse.ArgumentParser(description="YOLO training parameter parser")

    # Model parameters
    parser.add_argument("--model_name", type=str, default="yolov6n-p2", help="YOLO model name")
    
    # Data parameters
    parser.add_argument("--data", type=str, default="dms_action.yaml", help="Dataset configuration file")

    parser.add_argument("--dir_name", type=str, default=None, help="Dataset configuration file")

    # Training parameters
    parser.add_argument("--time", type=float, default=None, help="Training duration (hours)")
    parser.add_argument("--resume", action="store_true", help="Resume training from the last checkpoint")
    parser.add_argument("--epochs", type=int, default=100, help="Total number of training epochs")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size")
    parser.add_argument("--device", type=str, default="0", help="Training device (GPU ID or CPU)")
    parser.add_argument("--multi_scale", action="store_true", help="Enable multi-scale training")
    parser.add_argument("--weighted", action="store_true", help="Enable weighted image sampling based on class distribution")
    parser.add_argument("--cos_lr", action="store_true", help="Enable cosine learning rate scheduler")
    parser.add_argument("--bgr", type=float, default=0, help="Background augmentation ratio")
    parser.add_argument("--warmup_epochs", type=int, default=3.0, help="Number of warmup epochs")
    parser.add_argument("--lr0", type=float, default=0.01, help="Initial learning rate")
    parser.add_argument("--lrf", type=float, default=0.01, help="Final learning rate")
    parser.add_argument("--optimizer", type=str, choices=["SGD", "Adam", "AdamW"], default="SGD", help="Optimizer type")
    parser.add_argument("--close_mosaic", type=int, default=10, help="Disable mosaic augmentation after this number of epochs")
    
    # Logging and output parameters
    parser.add_argument("--project", type=str, default="runs", help="Directory to save training logs")

    return parser


def main(args):
    print("Called with args:")
    print(args)

    # Get the current date
    if args.dir_name is None:
        current_date = datetime.now().strftime("%Y%m%d")
        args.dir_name = current_date
    # Load YOLO model
    if args.resume:
        model = YOLO(f"{args.project}/{args.dir_name}_{args.model_name}/weights/last.pt")
    else:
        model = YOLO(f"{args.model_name}.yaml")
        

    # Start training
    model.train(
        data=args.data,
        time=args.time,
        resume=args.resume,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        project=args.project,
        name=f"{args.dir_name}_{args.model_name}",
        multi_scale=args.multi_scale,
        weighted=args.weighted,
        cos_lr=args.cos_lr,
        bgr=args.bgr,
        warmup_epochs=args.warmup_epochs,
        lr0=args.lr0,
        lrf=args.lrf,
        optimizer=args.optimizer,
        close_mosaic=args.close_mosaic
    )


if __name__ == '__main__':
    args = make_parser().parse_args()
    main(args)
