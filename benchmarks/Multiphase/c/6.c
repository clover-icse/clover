int main(){
    int x, y, z;

    // pre-conditions
    x = 1;
    y = 0;
    z = 0;

    // loop body
    while(unknown()){
        if(x > 0){
            y = y + 1;
        }else{
            z = z + 1;
        }
        x = -x;
        
    }

    // post-condition
    if((x == 1) && (y == 342341341)){
        assert(z == 342341341);
    }
    
}